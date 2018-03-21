"""
Manages the logging in of a user into the application,
and rejecting visitors that enter improper sign-in information.
"""
import json

from flask_login import current_user, login_user
from flask_restplus.reqparse import RequestParser
from werkzeug.exceptions import Unauthorized

import pydash_app.user


def login():
    if current_user.is_authenticated:
        result = {"message": "User already logged in"}
        return json.dumps(result)

    args = __parse_arguments()

    if 'username' not in args or 'password' not in args:
        result = {"message": "Username or password missing"}
        return json.dumps(result), 400

    user = pydash_app.user.authenticate(args['username'],
                                        args['password'])

    if not user:
        result = {"message": "Username or password incorrect"}
        return json.dumps(result), 401

    login_user(user)

    result = {"message": "User successfully logged in"}
    return json.dumps(result)


def __parse_arguments():
    parser = RequestParser()
    parser.add_argument('username')
    parser.add_argument('password')
    return parser.parse_args()
