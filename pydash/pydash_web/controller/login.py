"""
Manages the logging in of a user into the application,
and rejecting visitors that enter improper sign-in information.
"""
from flask import jsonify
from flask_login import current_user, login_user
from flask_restplus.reqparse import RequestParser

import pydash_app.user
#import pydash_app.impl.logger as pylog

#logger = pylog.Logger(__name__)


def login():
    #logger.info('Login requested')
    if current_user.is_authenticated:
        result = {
            "message": "User already logged in",
            "user": _user_details(current_user)
        }
        #logger.warning(f"Login failed - {current_user} already logged in")
        return jsonify(result)

    args = _parse_arguments()

    if 'username' not in args or 'password' not in args:
        result = {"message": "Username or password missing"}
        #logger.warning('Login failed - username or password missing')
        return jsonify(result), 400

    user = pydash_app.user.authenticate(args['username'],
                                        args['password'])

    if not user:
        result = {"message": "Username or password incorrect"}
        #logger.warning(f"Failed login request using {args['username']}, {args['password']}")
        return jsonify(result), 401

    login_user(user)
    #logger.info(f"{current_user} successfully logged in")

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