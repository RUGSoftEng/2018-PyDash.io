"""
Manages the logging in of a user into the application,
and rejecting visitors that enter improper sign-in information or have not been verified yet.
"""
from flask import jsonify, request
from flask_login import current_user, login_user

import pydash_app.user
import pydash_logger

logger = pydash_logger.Logger(__name__)


def login():
    logger.info('Login requested')
    if current_user.is_authenticated:
        result = {
            "message": "User already logged in",
            "user": _user_details(current_user)
        }
        logger.info(f"{current_user} already logged in")
        return jsonify(result)

    request_data = request.get_json(silent=True)

    if not request_data:
        logger.warning('Login failed - data missing')
        result = {'message': 'Data missing'}
        return jsonify(result), 400

    username = request_data.get('username')
    password = request_data.get('password')

    if username is None or password is None:
        result = {"message": "Username or password missing"}
        logger.warning('Login failed - username or password missing')
        return jsonify(result), 400

    user = pydash_app.user.authenticate(username, password)

    if not user:
        result = {"message": "Username or password incorrect"}
        logger.warning(f"Failed login request using {args['username']}, {args['password']}")
        return jsonify(result), 401

    if not user.is_verified():
        result = {"message": "User has not yet been verified"}
        logger.warning(f"Login failed - {user} has not yet been verified")
        return jsonify(result), 403

    login_user(user)
    logger.info(f"{current_user} successfully logged in")

    result = {
        "message": "User successfully logged in",
        "user": _user_details(user)
    }
    return jsonify(result)


def _user_details(user):
    return {
        "id": user.id,
        "username": user.name
    }
