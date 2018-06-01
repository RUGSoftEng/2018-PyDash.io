"""
Periodically pings a dashboard to see if the web service is still up.
"""

from functools import partial
from datetime import timedelta
import json

import requests

import flask_monitoring_dashboard_client
import pydash_app.dashboard.repository as dashboard_repository
import pydash_logger
import periodic_tasks

logger = pydash_logger.Logger(__name__)

_DEFAULT_PING_INTERVAL = timedelta(minutes=5)


def schedule_all_periodic_dashboard_pinging(
        interval=_DEFAULT_PING_INTERVAL,
        scheduler=periodic_tasks.default_task_scheduler):
    """
    Set up periodic dashboard pinging tasks for all dashboards that want their uptime to be monitored.
    :param interval: The frequency with which to ping a dashboard, defaults to 5 minutes.
    :param scheduler: The task scheduler to schedule the tasks to, defaults to the default scheduler.
    """
    for dashboard in dashboard_repository.all():
        schedule_periodic_dashboard_pinging(dashboard, interval, scheduler)


def schedule_periodic_dashboard_pinging(
        dashboard,
        interval=_DEFAULT_PING_INTERVAL,
        scheduler=periodic_tasks.default_task_scheduler):
    """
    Set up a periodic pinging task for a dashboard if the dashboard allows it.
    :param dashboard: The dashboard to set up a pinging task for.
    :param interval: The frequency with which to ping a dashboard, defaults to 5 minutes.
    :param scheduler: The task scheduler to schedule this task to, defaults to the default scheduler.
    """

    if dashboard.monitor_downtime:
        periodic_tasks.add_periodic_task(
            name=('dashboard', dashboard.id, 'pinging'),
            task=partial(_ping_dashboard, dashboard.id),
            interval=interval,
            scheduler=scheduler)


def _ping_dashboard(dashboard_id):
    try:
        dashboard = dashboard_repository.find(dashboard_id)
    except KeyError:
        logger.warning('Dashboard does not exist')
        return

    is_up = _is_dashboard_up(dashboard.url)
    dashboard.add_ping_result(is_up)

    dashboard_repository.update(dashboard)


def _is_dashboard_up(url):
    """
    Connect to a dashboard to see if it's up.
    :param url: The dashboard's URL.
    :return: True or False depending on whether the dashboard is up.
    """
    try:
        flask_monitoring_dashboard_client.get_details(url)
    except requests.exceptions.RequestException:
        return False
    except (json.JSONDecodeError, Exception):
        return True

    return True
