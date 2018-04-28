from functools import partial
from datetime import datetime, timedelta, timezone

import flask_monitoring_dashboard_client
from pydash_app.dashboard.endpoint import Endpoint
from pydash_app.dashboard.endpoint_call import EndpointCall
import pydash_app.dashboard.repository as dashboard_repository
import pydash_logger
import periodic_tasks

logger = pydash_logger.Logger(__name__)


def schedule_all_periodic_dashboards_tasks(
        interval=timedelta(hours=1),
        scheduler=periodic_tasks.default_task_scheduler):
    """
    Sets up all tasks that should be run periodically for each of the dashboards.
    (For now, that is only the EndpointCall fetching task.)

    """
    for dashboard in dashboard_repository.all():
        if dashboard.last_fetch_time is None:
            schedule_historic_dashboard_fetching(
                dashboard, scheduler=scheduler)
        else:
            schedule_periodic_dashboard_fetching(
                dashboard, interval=interval, scheduler=scheduler)


def schedule_periodic_dashboard_fetching(
        dashboard,
        interval=timedelta(hours=1),
        scheduler=periodic_tasks.default_task_scheduler):
    """
    Schedules the periodic EndpointCall fetching task for this dashboard.
    """
    logger.info(f'Creating periodic fetching task for {dashboard}')

    periodic_tasks.add_periodic_task(
        name=("dashboard", dashboard.id, "fetching"),
        task=partial(fetch_and_update_new_dashboard_info, dashboard.id),
        interval=interval,
        scheduler=scheduler)


def schedule_historic_dashboard_fetching(
        dashboard, scheduler=periodic_tasks.default_task_scheduler):
    """
    Schedules the fetching of historic EndpointCall information as a background task.
    The periodic fetching of new EndpointCall information is scheduled as soon as this task completes.
    """

    def task(dashboard_id):
        fetch_and_update_historic_dashboard_info(dashboard_id)
        schedule_periodic_dashboard_fetching(dashboard_id)

    periodic_tasks.add_background_task(
        name=("dashboard", dashboard.id, "historic_fetching"),
        task=partial(task, dashboard.id),
        scheduler=scheduler)


def fetch_and_update_new_dashboard_info(dashboard_id):
    """
    Updates the dashboard with the new EndpointCall information that is fetched from the Dashboard's remote location.
    """
    dashboard = dashboard_repository.find(dashboard_id)

    logger.info("INSIDE FETCH FUNCTION")

    fetch_and_add_endpoint_calls(dashboard)

    logger.info(f'{len(dashboard.endpoints)} endpoints found')
    logger.info(f'{len(dashboard._endpoint_calls)} endpoint calls')

    dashboard_repository.update(dashboard)

    logger.info(f'{len(dashboard.endpoints)} endpoints found')
    logger.info(f'{len(dashboard._endpoint_calls)} endpoint calls')

    logger.info(f"Dashboard {dashboard_id} updated.")


def fetch_and_update_historic_dashboard_info(dashboard_id):
    """
    Updates the dashboard with the historic EndpointCall information that is fetched from the Dashboard's remote location.
    """
    dashboard = dashboard_repository.find(dashboard_id)

    logger.info("INSIDE INITIAL DASHBOARD FETCHING FUNCTION")

    fetch_and_add_endpoints(dashboard)
    fetch_and_add_historic_endpoint_calls(dashboard)

    logger.info(f'{len(dashboard.endpoints)} endpoints found')
    logger.info(f'{len(dashboard._endpoint_calls)} historical endpoint calls')

    dashboard_repository.update(dashboard)

    logger.info(f'{len(dashboard.endpoints)} endpoints found')
    logger.info(f'{len(dashboard._endpoint_calls)} historical endpoint calls')


def fetch_and_add_endpoints(dashboard):
    """
    For a given dashboard, initialize it with the endpoints it has registered.
    Note that this will not add endpoint call data.
    :param dashboard: The dashboard to initialize with endpoints.
    """

    endpoints = _fetch_endpoints(dashboard)

    for endpoint in endpoints:
        dashboard.add_endpoint(endpoint)


def _fetch_endpoints(dashboard):
    """
    Fetches and returns a list of `Endpoint`s in the given dashboard.
    :param dashboard: The dashboard for which to fetch endpoints.
    :return: A list of `Endpoint`s for the dashboard.
    """

    monitor_rules = flask_monitoring_dashboard_client.get_monitor_rules(
        dashboard.url, dashboard.token)

    if monitor_rules is None:
        return []

    return [
        Endpoint(rule['endpoint'], rule['monitor']) for rule in monitor_rules
    ]


def fetch_and_add_historic_endpoint_calls(dashboard):
    """
    For a given dashboard, retrieve all historical endpoint calls and add them to it.
    :param dashboard: The dashboard to initialize with historical data.
    """

    # Only run this function if no periodic fetching of latest information has happened yet:
    if dashboard.last_fetch_time is not None:
        return

    details = flask_monitoring_dashboard_client.get_details(dashboard.url)
    first_request = int(details['first_request'])

    start_time = datetime.fromtimestamp(first_request, tz=timezone.utc)
    current_time = datetime.now(timezone.utc)

    while start_time < current_time:
        # TODO: for now historical data is pulled in chunks of 1 hour (hardcoded)
        end_time = start_time + timedelta(hours=1)

        if end_time > current_time:
            end_time = current_time

        endpoint_calls = _fetch_endpoint_calls(dashboard, start_time, end_time)

        if endpoint_calls is None:
            continue

        for call in endpoint_calls:
            dashboard.add_endpoint_call(call)
            dashboard.last_fetch_time = call.time

        start_time = end_time


def fetch_and_add_endpoint_calls(dashboard):
    """
    Retrieve the latest endpoint calls of the given dashboard and add them to it.
    :param dashboard: The dashboard for which to update endpoint calls.
    """

    logger.info(f"Updating endpoint calls for dashboard: {dashboard}")

    # Only run this function if historic fetching has happened.
    if dashboard.last_fetch_time is None:
        return

    new_calls = _fetch_endpoint_calls(
        dashboard, time_from=dashboard.last_fetch_time)

    logger.info(f"New endpoint calls: {new_calls}")

    if new_calls is []:
        return []

    for call in new_calls:
        dashboard.add_endpoint_call(call)

    dashboard.last_fetch_time = new_calls[-1].time

    logger.info(f"Saved to database: dashboard {dashboard}")


def _fetch_endpoint_calls(dashboard, time_from=None, time_to=None):
    """
    Fetches and returns a list of `EndpointCall`s for the given dashboard.
    :param dashboard: The dashboard for which to fetch endpoint calls.
    :param time_from: An operiodic_tasksional datetime indicating only data since that moment should be returned.
    :param time_to: An operiodic_tasksional datetime indicating only data up to that point should be returned.
    :return: A list of `EndpointCall`s containing the endpoint call data for this dashboard.
    """

    endpoint_requests = flask_monitoring_dashboard_client.get_data(
        dashboard.url, dashboard.token, time_from, time_to)

    if endpoint_requests is None:
        return []

    endpoint_calls = []
    for request in endpoint_requests:
        # The raw endpoint call data contains a timestamp formatted
        # as "yyyy-mm-dd hh:mm:ss.micro" so we need to parse it
        time = datetime.strptime(request['time'], '%Y-%m-%d %H:%M:%S.%f')
        time.replace(tzinfo=timezone.utc)

        call = EndpointCall(request['endpoint'], request['execution_time'],
                            time, request['version'], request['group_by'],
                            request['ip'])
        endpoint_calls.append(call)

    return endpoint_calls
