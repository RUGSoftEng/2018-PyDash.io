"""
Manages the logging in of a user into the application,
and rejecting visitors that enter improper sign-in information.
"""
from flask import jsonify
from flask_login import current_user, login_user
from flask_restplus.reqparse import RequestParser

import pydash_app.user
import pydash_app.impl.logger as pyLog

logger = pyLog.Logger()


def login():
    logger.info('Login requested')
    if current_user.is_authenticated:
        result = {
            "message": "User already logged in",
            "user": _user_details(current_user)
        }
        return jsonify(result)

    args = _parse_arguments()

    if 'username' not in args or 'password' not in args:
        result = {"message": "Username or password missing"}
        return jsonify(result), 400

    user = pydash_app.user.authenticate(args['username'],
                                        args['password'])

    if not user:
        result = {"message": "Username or password incorrect"}
        return jsonify(result), 401

    login_user(user)

    result = {
        "message": "User successfully logged in",
        "user": _user_details(user)
    }
    return jsonify(result)


def _parse_arguments():
    parser = RequestParser()
    parser.add_argument('username')
    parser.add_argument('password')
    return parser.parse_args()


def _user_details(user):
    return {
        "id": user.id,
        "username": user.name
    }