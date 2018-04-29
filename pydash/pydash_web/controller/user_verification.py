"""
Manages the verification of a User.
"""

from functools import wraps

from flask import jsonify
from flask_login import current_user
import pydash_app.user as user


def verify_user(verification_code):
    """
    Verifies the currently logged in User by comparing the given verification_code with the code assigned to the User.
    This is intended to be used only once, after the user has just registered their account in order to gain access to
    api-routes that have the `verification_required` decorator.
    :param verification_code: The verification code used to verify whether this verification is valid.
    """
    try:
        verified = user.verify(current_user.id, verification_code)
    except KeyError:
        result = {"message": "Corresponding user not found."}
        return jsonify(result), 409
    except user.AlreadyVerifiedError:
        result = {"message": "User already verified."}
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
            return jsonify(message), 403  # Not sure if a jsonified message is the right return value for now.
    return decorated_view(func)
