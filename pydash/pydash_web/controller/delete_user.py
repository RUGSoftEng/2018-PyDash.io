"""
Manages deletion of a user.
"""

from flask import jsonify
from flask_login import current_user

import pydash_app.user as user
import pydash_app.dashboard as dashboard
import pydash_logger.logger as pylog

logger = pylog.Logger(__name__)


def delete_user():
    """
    Deletes the currently logged in user and all dashboards they own.
    """

    try:
        user.remove_from_repository(current_user.id)
    except KeyError:
        result = {'message': 'User not found in database.'}
        logger.warning(f'Delete_user failed - {current_user} was not found in the database.')
        return jsonify(result), 500

    for dash in dashboard.dashboards_of_user(current_user.id):
        try:
            dashboard.remove_from_repository(dash)
        except KeyError:
            logger.warning(f'Dashboard {dash} from user {current_user} has already been removed.')

    logger.info(f'{current_user} deleted themselves successfully.')

    result = {'message': f'User {current_user} successfully deleted themselves.'}
    return jsonify(result), 200
