"""
Manages the lookup and returning of dashboard information for a certain user.

Currently only returns static mock data.
"""

from flask import jsonify
from flask_login import current_user
from pydash_app.dashboard.dashboard import DashboardState

import pydash_app.dashboard
import pydash_logger

# from pydash_app.fetching.dashboard_fetch import update_endpoint_calls, _fetch_endpoint_calls

logger = pydash_logger.Logger(__name__)


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

        # logger.debug(f'Amount of newly fetched endpoint calls: {len(_fetch_endpoint_calls(db, db.last_fetch_time))}')

        # update_endpoint_calls(db)
    except KeyError:
        logger.warning(f"Could not find dashboard matching with {dashboard_id}")
        return jsonify({"message": "Could not find a matching dashboard."}), 404
    except ValueError:  # Happens when called without a proper UUID
        logger.warning(f"Invalid dashboard_id: {dashboard_id}")
        return jsonify({"message": "Invalid dashboard_id"}), 400

    if db.user_id != current_user.id:
        logger.warning(F"{current_user} is not authorised to view {db}")
        return jsonify({"message": "Not authorised to view this dashboard."}), 403

    logger.info(f"Retrieved dashboard {db}")
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
    logger.info(f"Retrieving list of dashboards for {current_user}")
    dashboards = pydash_app.dashboard.dashboards_of_user(current_user.id)

    return jsonify([_simple_dashboard_detail(dashboard) for dashboard in dashboards]), 200


def _simple_dashboard_detail(dashboard):
    """
    Returns a simple representation of the given dashboard.
    :param dashboard: The Dashboard-entity in question.
    :return: A dict structured as the simple JSON-representation of the given dashboard.
    """

    def endpoint_dict(endpoint):
        return {
            'name': endpoint.name,
            'enabled': endpoint.is_monitored
        }

    endpoints = [endpoint_dict(endpoint) for endpoint in dashboard.endpoints.values()]

    dashboard_data = {
        'id': dashboard.id,
        'url': dashboard.url,
        'endpoints': endpoints
    }

    if dashboard.name is not None:
        dashboard_data['name'] = dashboard.name

    if str(dashboard.state.name).split("_")[-1] == "failure":
        dashboard_data['error'] = dashboard.error

    return dashboard_data


def _dashboard_detail(dashboard):
    """
    Returns the representation of the given dashboard in detail.
    :param dashboard: The Dashboard-entity in question.
    :return: A dict structured as the JSON-representation of the given dashboard.
    """

    def endpoint_dict(endpoint):
        return {
            'name': endpoint.name,
            'aggregates': endpoint.aggregated_data(),
            'enabled': endpoint.is_monitored
        }

    endpoints = [endpoint_dict(endpoint) for endpoint in dashboard.endpoints.values()]

    dashboard_data = {
        'id': dashboard.id,
        'url': dashboard.url,
        'aggregates': dashboard.aggregated_data(),
        'endpoints': endpoints
    }

    if dashboard.name is not None:
        dashboard_data['name'] = dashboard.name

    if str(dashboard.state.name).split("_")[-1] == "failure":
        dashboard_data['error'] = dashboard.error

    return dashboard_data
