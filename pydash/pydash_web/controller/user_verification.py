"""
Manages the verification of a User.
"""

from flask import jsonify
from flask_restplus.reqparse import RequestParser
import pydash_app.user as user
import pydash_logger

logger = pydash_logger.Logger(__name__)

# For now verify_user will have input parameters, until the verification link points to a front-end page that can do a post-request.
def verify_user():
    """
    Verifies the currently logged in User by comparing the given verification_code with the code assigned to the User.
    This is intended to be used only once, after the user has just registered their account in order to gain access to
    api-routes that have the `verification_required` decorator.
    """

    args = _parse_arguments()
    if not args['verification_code']:
        result = {"message": "Verification code missing"}
        logger.warning('Verification failed - verification_code missing')
        return jsonify(result), 400
    verification_code = args['verification_code']

    try:
        user.verify(verification_code)
    except user.verification.InvalidVerificationCodeError:
        result = {"message": "Invalid verification code."}
        return jsonify(result), 400
    except user.verification.VerificationCodeExpiredError:
        result = {"message": "Verification code expired."}
        return jsonify(result), 400

    result = {"message": "User successfully verified."}
    return jsonify(result), 200


def _parse_arguments():
    parser = RequestParser()
    parser.add_argument('verification_code')
    return parser.parse_args()
