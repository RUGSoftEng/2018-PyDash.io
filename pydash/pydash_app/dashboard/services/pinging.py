"""
Periodically pings a dashboard to see if the web service is still up.
"""

import flask_monitoring_dashboard_client
import pydash_app.dashboard.repository as dashboard_repository
import pydash_logger

logger = pydash_logger.Logger(__name__)


def _ping_dashboard(dashboard_id):
    try:
        dashboard = dashboard_repository.find(dashboard_id)
    except KeyError:
        logger.warning('Dashboard does not exist')
        return

    try:
        flask_monitoring_dashboard_client.get_details(dashboard.url)
    except Exception:
        return False

    return True
