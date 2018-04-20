"""
Manages the registration of a new user.
"""

from flask import jsonify
import pydash_app.user
import pydash_app.impl.logger as pylog

logger = pylog.Logger(__name__)


def register_user(name, password):
    user = pydash_app.user.User(name, password)
    if pydash_app.user.find_by_name(name) is not None:
        message = f'User with name {name} already exists.'
        logger.warning(f'While registering a user: {message}')
        return jsonify(message), 409  # Todo: perhaps return 400 instead?
    else:
        pydash_app.user.add_to_repository(user)

    message = 'User successfully registered.'
    return jsonify(message), 200
