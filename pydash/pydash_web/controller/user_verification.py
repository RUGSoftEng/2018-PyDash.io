"""
Manages the verification of a User.
"""

from functools import wraps

from flask import jsonify
from flask_login import current_user
import pydash_app.user as user


def verify_user(verification_code):
    try:
        user_to_verify = user.find(current_user.id)
    except KeyError:
        result = {"message": "Corresponding user not found."}
        return jsonify(result), 409

    if str(verification_code) != user_to_verify.get_verification_code():
        result = {"message": "Invalid verification code."}
        return jsonify(result), 400

    user_to_verify.isVerified = True
    user.repository.update(user_to_verify)

    result = {"message": "User successfully verified."}
    return jsonify(result), 200


def verification_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if current_user.is_active():
            return func(*args, **kwargs)
        else:
            message = {'message': 'Account has not been verified yet.'}
            return jsonify(message), 403  # Not sure if a jsonified message is the right return value for now.
    return decorated_view(func)
