"""
Allows retrieval of dashboard downtime information.
"""

from flask import jsonify
from flask_login import current_user

import pydash_app.dashboard
import pydash_logger

logger = pydash_logger.Logger(__name__)


def dashboard_downtime(dashboard_id):
    try:
        dashboard = pydash_app.dashboard.find(dashboard_id)
    except KeyError:
        result = {'message': f'Dashboard_id {dashboard_id} is not found.'}
        logger.warning(f'Dashboard downtime failure - Dashboard_id {dashboard_id} is not found. '
                       f'Current user: {current_user}')
        return jsonify(result), 400
    except ValueError:  # Happens when called without a proper UUID
        result = {'message': f'Dashboard_id {dashboard_id} is invalid UUID.'}
        logger.warning(f'Dashboard downtime failure - Dashboard_id {dashboard_id} is invalid UUID. '
                       f'Current user: {current_user}')
        return jsonify(result), 400

    if str(dashboard.user_id) != str(current_user.id):
        result = {'message': f'Current user is not allowed to access dashboard {dashboard_id}'}
        logger.warning(f'Dashboard downtime failure - '
                       f'User {current_user} is not allowed to access dashboard {dashboard_id}')
        return jsonify(result), 403


def _downtime_data(dashboard):
    data = dashboard.get_downtime_data()
