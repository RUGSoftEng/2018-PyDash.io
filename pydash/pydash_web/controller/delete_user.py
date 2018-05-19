"""
Manages deletion of a user.
"""

from flask import jsonify, request
from flask_login import current_user

import pydash_app.user as user
import pydash_app.dashboard as dashboard
import pydash_logger.logger as pylog

logger = pylog.Logger(__name__)


def delete_user():
    """
    Deletes the currently logged in user and all dashboards they own.
    """

    request_data = request.get_json(silent=True)

    if not request_data:
        logger.warning('Login failed - data missing')
        result = {'message': 'Data missing'}
        return jsonify(result), 400

    password = request_data.get('password')

    if password is None:
        logger.error('Delete_user failed - no password provided')
        result = {'message': 'Deletion failed - no password provided'}
        return jsonify(result), 400

    if not current_user.check_password(password):
        logger.error('Delete_user failed - wrong password provided')
        result = {'message': 'Deletion failed - password incorrect'}
        return jsonify(result), 401

    # TODO: make sure to not delete the dashboard if it is shared between users
    for dash in dashboard.dashboards_of_user(current_user.id):
        try:
            dashboard.remove_from_repository(dash)
        except KeyError:
            logger.warning(f'Dashboard {dash} from user {current_user} has already been removed.')

    try:
        user.remove_from_repository(current_user.id)
    except KeyError:
        result = {'message': 'User not found in database.'}
        logger.warning(f'Delete_user failed - {current_user} was not found in the database.')
        return jsonify(result), 500

    logger.info(f'{current_user} deleted themselves successfully.')

    result = {'message': f'User {current_user} successfully deleted themselves.'}
    return jsonify(result), 200
