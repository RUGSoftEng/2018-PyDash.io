"""
Manages the registration of a new user.
"""

from flask import jsonify
from flask_restplus.reqparse import RequestParser

import pydash_app.user
import pydash_app.impl.logger as pylog


logger = pylog.Logger(__name__)


def register_user():
    args = _parse_arguments()

    username = args['username']
    password = args['password']

    print(f'args={args}')

    if not username or not password:
        message = {'message': 'Username or password missing'}
        logger.warning('User registration failed - username or password missing')
        return jsonify(message), 400

    if pydash_app.user.find_by_name(username) is not None:
        message = {'message': f'User with username {username} already exists.'}
        logger.warning(f'While registering a user: {message}')
        return jsonify(message), 409  # Todo: perhaps return 400 instead?
    else:
        user = pydash_app.user.User(username, password)
        pydash_app.user.add_to_repository(user)
        message = {'message': 'User successfully registered.'}
        logger.info(f'User successfully registered with username: {username}')
        return jsonify(message), 200


def _parse_arguments():
    parser = RequestParser()
    parser.add_argument('username')
    parser.add_argument('password')
    return parser.parse_args()
