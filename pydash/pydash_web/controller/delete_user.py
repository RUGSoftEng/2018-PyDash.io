"""
Manages deletion of a user.
"""

from flask import jsonify
from flask_login import current_user

from pydash_app.user import find, remove_from_repository as remove_from_user_repository
from pydash_app.dashboard import dashboards_of_user, remove_from_repository as remove_from_dashboard_repository
import pydash_app.impl.logger as pylog

logger = pylog.Logger(__name__)


def delete_user():
    """
    Deletes the currently logged in user and all dashboards they own.
    """

    try:
        user = find(current_user.id)
        remove_from_user_repository(user)
    except KeyError or UnboundLocalError:  # UnboundLocalError will be thrown as well, due to the use of `user`.
        result = {'message': 'User not found in database.'}
        logger.warning(f'Delete_user failed - {current_user} was not found in the database.')
        return jsonify(result), 500

    for dashboard in dashboards_of_user(current_user.id):
        try:
            remove_from_dashboard_repository(dashboard)
        except KeyError:
            logger.warning(f'Dashboard {dashboard} from user {user} has already been removed.')

    logger.info(f'{user} deleted themselves successfully.')

    result = {'message': 'User successfully deleted themselves.'}
    return jsonify(result), 200
