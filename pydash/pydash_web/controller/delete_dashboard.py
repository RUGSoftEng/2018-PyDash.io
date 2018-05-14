"""
Manages the deletion of a dashboard.
"""

from flask import jsonify
from flask_login import current_user

import pydash_app.dashboard
import pydash_logger

logger = pydash_logger.Logger(__name__)


def delete_dashboard(dashboard_id):
    try:
        dashboard = pydash_app.dashboard.find(dashboard_id)
    except KeyError:
        logger.warning(f"Could not find dashboard matching with {dashboard_id}")
        return jsonify({"message": "Could not find a matching dashboard"}), 404
    except ValueError:  # Happens when called without a proper UUID
        logger.warning(f"Invalid dashboard_id: {dashboard_id}")
        return jsonify({"message": "Invalid dashboard_id"}), 400

    if dashboard.user_id != current_user.id:
        logger.warning(f"{current_user} is not authorised to view {dashboard}")
        return jsonify({"message": "Not authorised to delete this dashboard"}), 403

    try:
        # TODO: only remove if owned by one user, otherwise just remove the user's id from the dashboard
        pydash_app.dashboard.remove_from_repository(dashboard)
    except KeyError:
        logger.warning(f'Dashboard {dashboard} does not seem to exist in the database')
        jsonify({"message": "Could not find a matching dashboard"}), 404

    result = {'message': 'Successfully removed dashboard'}
    return jsonify(result), 200
