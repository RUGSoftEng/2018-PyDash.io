"""
Manages the verification of a User.
"""

from flask import jsonify, request
import pydash_app.user as user
import pydash_logger

logger = pydash_logger.Logger(__name__)


def verify_user():
    """
    Verifies the currently logged in User by comparing the given verification_code with the code assigned to the User.
    This is intended to be used only once, after the user has just registered their account in order to gain access to
    api-routes that have the `verification_required` decorator.
    """

    request_data = request.get_json(silent=True)

    if not request_data:
        logger.warning('Login failed - data missing')
        result = {'message': 'Data missing'}
        return jsonify(result), 400

    verification_code = request_data.get('verification_code')

    if verification_code is None:
        logger.warning('Verification failed - verification code missing')
        result = {'message': 'Verification code missing'}
        return jsonify(result), 400

    if not verification_code:
        logger.warning('Verification failed - verification code cannot be empty')
        result = {'message': 'Verification code cannot be empty'}
        return jsonify(result), 400

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
