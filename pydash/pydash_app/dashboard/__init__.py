
"""
This module is the public interface (available to the web-application pydash_web)
for interacting with Dashboards.
"""
from .dashboard import Dashboard
import pydash_app.dashboard.dashboard_repository

# TODO: As soon as PydashWeb requests data from the dashboard,
# use this module as intermediary between pydash_web and the dashboard_repository
