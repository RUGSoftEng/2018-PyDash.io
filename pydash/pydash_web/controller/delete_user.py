"""
Manages deletion of a user.
"""

from flask import jsonify
from flask_login import current_user

import pydash_app.user
import pydash_app.impl.logger as pylog

logger = pylog.Logger(__name__)


def delete_user():
    if not current_user.is_authenticated():  # Note: Will this even happen?
        result = {'message': 'User was not logged in.'}
        logger.warning(f'Delete_user failed - {current_user} was not logged in.')
        return jsonify(result), 401

    maybe_user = pydash_app.user.maybe_find_user(current_user.id)
    if maybe_user is None:
        result = {'message': 'User not found in database.'}
        logger.warning(f'Delete_user failed - {current_user} was not found in the database.')
        return jsonify(result), 500

    try:  # In case the database has been updated right in between the previous check.
        pydash_app.user.remove_from_repository(maybe_user)
    except KeyError:
        result = {'message': 'User not found in database.'}
        logger.warning(f'Delete_user failed - {current_user} was not found in the database.')
        return jsonify(result), 500

    logger.info(f'{current_user} deleted themselves successfully.')
    result = {'message': 'User successfully deleted themselves.'}
    jsonify(result), 200
