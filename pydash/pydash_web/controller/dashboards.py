"""
Manages the lookup and returning of dashboard information for a certain user.

Currently only returns static mock data.
"""

from flask import jsonify
from flask_login import current_user

import pydash_app.dashboard


def dashboard(dashboard_id):
    """
    Lists information of a single dashboard.
    :param dashboard_id: ID of the dashboard to return.
    :return: A tuple containing:
             - A dict, containing the dashboard details of the current user's dashboards.
               or
               A dict containing an error message describing the particular error.
             - A corresponding HTML status code.
    """
    try:
        db = pydash_app.dashboard.find(dashboard_id)
    except KeyError:
        return jsonify({"message": "Could not find a matching dashboard."}), 500
    except ValueError:  # Happens when called without a proper UUID
        return jsonify({"message": "Invalid dashboard_id"}), 400

    if db.user_id != current_user.id:
        return jsonify({"message": "Not authorised to view this dashboard."}), 403

    return jsonify(_dashboard_detail(db)), 200


def dashboards():
    """
    Lists the dashboards of the current user.
    :return: A tuple containing:
             - A list of dicts, containing dashboard details of the current user's dashboards.
               or
               A dict containing an error message describing the particular error.
             - A corresponding HTML status code.
    """
    dbs = pydash_app.dashboard.dashboards_of_user(current_user.id)

    return jsonify([_dashboard_detail(db) for db in dbs]), 200


def _dashboard_detail(db):
    """
    Returns the representation of the given dashboard in detail.
    :param db: The Dashboard-entity in question.
    :return: A dict structured as the JSON-representation of the given dashboard.
    """

    def endpoint_dict(endpoint):
        return {
            'name': endpoint.name,
            'aggregates': endpoint.aggregated_data(),
            'enabled': endpoint.is_monitored
        }

    endpoints_dict = [endpoint_dict(endpoint) for endpoint in db.endpoints.values()]
    return {
        'id': db.id,
        'url': db.url,
        'aggregates': db.aggregated_data(),
        'endpoints': endpoints_dict
    }
