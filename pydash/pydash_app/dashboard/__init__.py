"""
This module is the public interface (available to the web-application pydash_web)
for interacting with Dashboards.
"""
from .entity import Dashboard
from flask import jsonify
from flask_login import current_user

import pydash_logger
import pydash_app.dashboard.repository

logger = pydash_logger.Logger(__name__)


def add_to_repository(dashboard):
    try:
        repository.add(dashboard)
    except KeyError:
        raise


def remove_from_repository(dashboard):
    try:
        repository.delete(dashboard)
    except KeyError:
        raise


def find(dashboard_id):
    """
    Returns a single Dashboard-entity with the given UUID or None if it could not be found.
    :param dashboard_id: UUID of the dashboard we hope to find.
    :return: The Dashboard-entity with the given UUID or raises an Exception if it could not be found.
    """
    return repository.find(dashboard_id)


def dashboards_of_user(user_id):
    """
    Returns a list of Dashboard-entities that are connected to the given user.
    :param user_id: The UUID of the user whose dashboards we're requesting.
    :return: A list of Dashboard-entities.
    """
    return [db for db in repository.all() if db.user_id == user_id]


def find_verified_dashboard(dashboard_id):
    """
    Verifies if a given dashboard_id is correct and if the current user has access
    to the dashboard.
    :param dashboard_id: The UUID of the dashboard to be validated.
    :return: True if the dashboard is valid, else False followed by the result and
    the http error code.
    """

    try:
        dashboard = pydash_app.dashboard.find(dashboard_id)
    except KeyError:
        result = {'message': f'Dashboard_id {dashboard_id} is not found.'}
        logger.warning(f'Endpoint_boxplots failure - Dashboard_id {dashboard_id} is not found. '
                       f'Current user: {current_user}')
        return None, jsonify(result), 404
    except ValueError:  # Happens when called without a proper UUID
        result = {'message': f'Dashboard_id {dashboard_id} is invalid UUID.'}
        logger.warning(f'Endpoint_boxplots failure - Dashboard_id {dashboard_id} is invalid UUID. '
                       f'Current user: {current_user}')
        return None, jsonify(result), 400

    # Check user authorisation
    if str(dashboard.user_id) != str(current_user.id):
        result = {'message': f'Current user is not allowed to access dashboard {dashboard_id}'}
        logger.warning(f'Endpoint_boxplots failure - '
                       f'User {current_user} is not allowed to access dashboard {dashboard_id}')
        return None, jsonify(result), 403

    return dashboard, None, None
