"""
Manages the deletion of a dashboard.
"""

from flask import jsonify
from pydash_app.dashboard import verify_dashboard, find, remove_from_repository

import pydash_logger

logger = pydash_logger.Logger(__name__)


def delete_dashboard(dashboard_id):
    # Check dashboard_id
    valid_dashboard, result, http_error = verify_dashboard(dashboard_id)

    if not valid_dashboard:
        return result, http_error
    
    dashboard = find(dashboard_id)

    try:
        # TODO: only remove if owned by one user, otherwise just remove the user's id from the dashboard
        remove_from_repository(dashboard)
    except KeyError:
        logger.warning(f'Dashboard {dashboard} does not seem to exist in the database')
        jsonify({"message": "Could not find a matching dashboard"}), 404

    result = {'message': 'Successfully removed dashboard'}
    return jsonify(result), 200
