"""
This module is the public interface (available to the web-application pydash_web)
for interacting with Dashboards.
"""
from .dashboard import Dashboard
import pydash_app.dashboard.dashboard_repository


def find(dashboard_id):
    """
    Returns a single Dashboard-entity with the given UUID or None if it could not be found.
    :param dashboard_id: UUID of the dashboard we hope to find.
    :return: The Dashboard-entity with the given UUID or None if it could not be found.
    """
    return dashboard_repository.find(dashboard_id)


def dashboards_of_user(user_id):
    """
    Returns a list of Dashboard-entities that are connected to the given user.
    :param user_id: The UUID of the user whose dashboards we're requesting.
    :return: A list of Dashboard-entities.
    """
    return [db for db in dashboard_repository.all() if db.user_id == user_id]

# TODO: As soon as PydashWeb requests data from the dashboard,
# use this module as intermediary between pydash_web and the dashboard_repository
