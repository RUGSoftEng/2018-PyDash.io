"""
Manages the verification of a User.
"""

from functools import wraps

from flask import jsonify
from flask_login import current_user
from flask_restplus.reqparse import RequestParser
import pydash_app.user as user
import pydash_logger

logger = pydash_logger.Logger(__name__)

# For now verify_user will have input parameters, until the verification link points to a front-end page that can do a post-request.
def verify_user(verification_code):
    """
    Verifies the currently logged in User by comparing the given verification_code with the code assigned to the User.
    This is intended to be used only once, after the user has just registered their account in order to gain access to
    api-routes that have the `verification_required` decorator.
    """

    # args = _parse_arguments()
    # if 'verification_code' not in args:
    #     result = {"message": "Verification code missing"}
    #     logger.warning('Verification failed - verification_code missing')
    #     return jsonify(result), 400
    # verification_code = args['verification_code']

    try:
        verified = user.verify(verification_code)
    except user.verification.InvalidVerificationCodeError:
        result = {"message": "Invalid verification code."}
        return jsonify(result), 400
    except user.verification.VerificationCodeExpiredError:
        result = {"message": "Verification code expired."}
        return jsonify(result), 400

    if not verified:
        result = {"message": "Invalid verification code."}
        return jsonify(result), 400

    result = {"message": "User successfully verified."}
    return jsonify(result), 200


def verification_required(func):
    """
    Decorator for checking whether the currently logged in user has been verified.
    :param func: The function to decorate.
    """
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if current_user.is_verified():
            return func(*args, **kwargs)
        else:
            message = {'message': 'User has not been verified yet.'}
            return jsonify(message), 403  # Not sure if returning a jsonified message might break the application.
    return decorated_view


def _parse_arguments():
    parser = RequestParser()
    parser.add_argument('verification_code')
    return parser.parse_args()
