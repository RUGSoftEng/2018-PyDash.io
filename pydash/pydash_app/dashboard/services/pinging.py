"""
Periodically pings a dashboard to see if the web service is still up.
"""

from datetime import timedelta

import flask_monitoring_dashboard_client
import pydash_app.dashboard.repository as dashboard_repository
import pydash_logger
import periodic_tasks

logger = pydash_logger.Logger(__name__)

def schedule_periodic_dashboard_pinging(
        interval=timedelta(hours=1),
        scheduler=periodic_tasks.default_task_scheduler):
    """
    Set up periodic dashboard pinging tasks
    """
    for dashboard in dashboard_repository.all():
        if dashboard.monitor_uptime:
            periodic_tasks.add_periodic_task(
                name=("dashboard", dashboard.id, "pinging"),
                task=partial(_ping_dashboard, dashboard.id),
                interval=interval,
                scheduler=scheduler)


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
