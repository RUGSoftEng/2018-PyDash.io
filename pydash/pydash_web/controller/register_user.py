"""
Manages the registration of a new user.
"""

from flask import jsonify
from flask_restplus.reqparse import RequestParser

import pydash_app.user
import pydash_logger


logger = pydash_logger.Logger(__name__)

MINIMUM_PASSWORD_LENGTH = 7


def register_user():
    args = _parse_arguments()

    username = args['username']
    password = args['password']

    print(f'args={args}')

    if not username or not password:
        message = {'message': 'Username or password missing'}
        logger.warning('User registration failed - username or password missing')
        return jsonify(message), 400

    if not _check_password_requirements(password):
        message = {'message': 'Password should consist of at least 7 characters, contain at least one capital letter'
                              ' and at least one digit.'}
        logger.warning('User registration failed - password does not conform to the requirements.')
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


def _check_password_requirements(password):
    rules = [lambda xs: any(x.isupper() for x in xs),
             lambda xs: any(x.isdigit() for x in xs),
             lambda xs: len(xs) >= MINIMUM_PASSWORD_LENGTH
             ]

    if all(rule(password) for rule in rules):
        return True
    else:
        return False
