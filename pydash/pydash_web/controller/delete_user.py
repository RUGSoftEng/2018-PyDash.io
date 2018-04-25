"""
Manages deletion of a user.
"""

from flask import jsonify
from flask_login import current_user

from pydash_app.user import maybe_find_user, remove_from_repository as remove_from_user_repository
from pydash_app.dashboard import dashboards_of_user, remove_from_repository as remove_from_dashboard_repository
import pydash_app.impl.logger as pylog

logger = pylog.Logger(__name__)


def delete_user():
    """
    Deletes the currently logged in user and all dashboards they own.
    """

    maybe_user = maybe_find_user(current_user.id)
    if maybe_user is None:
        result = {'message': 'User not found in database.'}
        logger.warning(f'Delete_user failed - {current_user} was not found in the database.')
        return jsonify(result), 500

    try:  # In case the database has been updated right in between the previous check.
        remove_from_user_repository(maybe_user)
    except KeyError:
        result = {'message': 'User not found in database.'}
        logger.warning(f'Delete_user failed - {maybe_user} was not found in the database.')
        return jsonify(result), 500

    for dashboard in dashboards_of_user(current_user.id):
        try:
            remove_from_dashboard_repository(dashboard)
        except KeyError:
            logger.warning(f'Dashboard {dashboard} from user {maybe_user} has already been removed.')

    logger.info(f'{current_user} deleted themselves successfully.')

    result = {'message': 'User successfully deleted themselves.'}
    return jsonify(result), 200
