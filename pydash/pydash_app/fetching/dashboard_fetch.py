from datetime import datetime, timedelta

from pydash_app.impl.fetch import get_monitor_rules, get_data, get_details
from pydash_app.dashboard.endpoint import Endpoint
from pydash_app.dashboard.endpoint_call import EndpointCall
from pydash_app.dashboard.dashboard_repository import update as update_dashboard

import pydash_app.impl.periodic_tasks as pt
from functools import partial


def initialise_dashboard_fetching(dashboard, interval=timedelta(hours=1), scheduler=pt.default_task_scheduler):
    """
    Initialise a dashboard from its remote endpoints and add them to the scheduler, with the given interval.
    This also fetches and stores all historical data up to this point in time.
    :param dashboard: The Dashboard to initialise.
    :param interval: The interval at which the endpoints should be fetched. This should be a datetime.timedelta object.
     Defaults to 1 hour.
    :param scheduler: The scheduler to add the fetch calls to.
     Defaults to the default TaskScheduler provided in the pydash_app.impl.periodic_tasks package.
    """
    initialize_endpoints(dashboard)
    initialize_endpoint_calls(dashboard)

    for endpoint in dashboard.endpoints:
        _add_endpoint_to_fetch_from(dashboard, endpoint, interval, scheduler)


def update_dashboard_fetching(dashboard, interval=timedelta(hours=1), scheduler=pt.default_task_scheduler,
                              override_previous_endpoint_interval=True):
    """
    Update a dashboard from its remote endpoints and update their fetching w.r.t the scheduler, with the given interval.
    :param dashboard: The Dashboard to update.
    :param interval: The interval at which the endpoints should be fetched. This should be a datetime.timedelta object.
     Defaults to 1 hour.
    :param scheduler: The scheduler to add the fetch calls to.
     Defaults to the default TaskScheduler provided in the pydash_app.impl.periodic_tasks package.
    :param override_previous_endpoint_interval: A Boolean to indicate whether the user wishes to override the interval
     of all other endpoint-fetching connected to this dashboard. Defaults to True.
    """
    old_endpoints = set([dashboard.endpoints[key] for key in dashboard.endpoints])
    new_endpoints = set(_fetch_endpoints(dashboard))

    additions = new_endpoints.difference(old_endpoints)
    deletions = old_endpoints.difference(new_endpoints)
    equivalents = old_endpoints.intersection(new_endpoints)

    # Override
    if override_previous_endpoint_interval:
        for endpoint in equivalents:
            _add_endpoint_to_fetch_from(dashboard, endpoint, interval, scheduler)

    # Add new endpoints
    for endpoint in additions:
        _add_endpoint_to_fetch_from(dashboard, endpoint, interval, scheduler)
        dashboard.add_endpoint(endpoint)

    # Remove deleted endpoints
    for endpoint in deletions:
        _remove_endpoint_to_fetch_from(dashboard, endpoint, scheduler)
        dashboard.remove_endpoint(endpoint)

    # Notify dashboard_repository
    update_dashboard(dashboard)


def _add_endpoint_to_fetch_from(dashboard, endpoint, interval=timedelta(hours=1), scheduler=pt.default_task_scheduler):
    """
    Adds the fetching of data from `endpoint` of `dashboard` to the given scheduler.
    :param dashboard: The Dashboard this Endpoint belongs to.
    :param endpoint: The Endpoint in question.
    :param interval: The datetime.timedelta object indicating the interval of the fetching.
     Defaults to 1 hour.
    :param scheduler: The TaskScheduler we want to add this Endpoint-fetching to.
     Defaults to the default scheduler that is provided in the pydash_app.impl.periodic_tasks package.
    """

    pt.add_periodic_task(name=str(dashboard.url) + "/" + str(endpoint.name),  # key='<url>/<endpoint>'
                         interval=interval,
                         task=partial(update_endpoint_calls, dashboard),
                         scheduler=scheduler
                         )


def _remove_endpoint_to_fetch_from(dashboard, endpoint, scheduler=pt.default_task_scheduler):
    """
    Removes an endpoint from the scheduler for that specific dashboard.
    :param dashboard: The Dashboard the endpoint belongs to.
    :param endpoint: The Endpoint itself.
    :param scheduler: The TaskScheduler to remove it from.
     Defaults to the default scheduler that is provided in the pydash_app.impl.periodic_tasks package.
    """
    pt.remove_task(name=str(dashboard.url) + "/" + str(endpoint.name), scheduler=scheduler)


def initialize_endpoints(dashboard):
    """
    For a given dashboard, initialize it with the endpoints it has registered.
    Note that this will not add endpoint call data.
    :param dashboard: The dashboard to initialize with endpoints.
    """

    endpoints = _fetch_endpoints(dashboard)
    for endpoint in endpoints:
        dashboard.add_endpoint(endpoint)

    update_dashboard(dashboard)


def _fetch_endpoints(dashboard):
    """
    Fetches and returns a list of `Endpoint`s in the given dashboard.
    :param dashboard: The dashboard for which to fetch endpoints.
    :return: A list of `Endpoint`s for the dashboard.
    """

    # TODO: this function does not actually put the data into the dashboard yet, only returns it

    monitor_rules = get_monitor_rules(dashboard.url, dashboard.token)

    if monitor_rules is None:
        return None

    return [Endpoint(rule['endpoint'], rule['monitor']) for rule in monitor_rules]


def initialize_endpoint_calls(dashboard):
    """
    For a given dashboard, retrieve all historical endpoint calls and store them in the database.
    :param dashboard: The dashboard to initialize with historical data.
    """

    if dashboard.last_fetch_time is not None:
        return

    details = get_details(dashboard.url)
    first_request = int(details['first_request'])

    start_time = datetime.fromtimestamp(first_request)
    current_time = datetime.utcnow()

    while start_time < current_time:
        # TODO: for now historical data is pulled in chunks of 1 hour (hardcoded)
        end_time = start_time + timedelta(hours=1)

        endpoint_calls = _fetch_endpoint_calls(dashboard, start_time, end_time)
        for call in endpoint_calls:
            dashboard.add_endpoint_call(call)

        start_time = end_time

    update_dashboard(dashboard)


def update_endpoint_calls(dashboard):
    """
    Retrieve the latest endpoint calls of the given dashboard and store them in the database.
    :param dashboard: The dashboard for which to update endpoint calls.
    """

    fetch_start_time = datetime.utcnow()

    if dashboard.last_fetch_time is None:
        return

    new_calls = _fetch_endpoint_calls(dashboard, dashboard.last_fetch_time)
    for call in new_calls:
        dashboard.add_endpoint_call(call)

    dashboard.last_fetch_time = fetch_start_time

    update_dashboard(dashboard)


def _fetch_endpoint_calls(dashboard, time_from=None, time_to=None):
    """
    Fetches and returns a list of `EndpointCall`s for the given dashboard.
    :param dashboard: The dashboard for which to fetch endpoint calls.
    :param time_from: An optional timestamp indicating only data since that timestamp should be returned.
    :param time_to: An optional timestamp indicating only data up to that timestamp should be returned.
    :return: A list of `EndpointCall`s containing the endpoint call data for this dashboard.
    """

    endpoint_requests = get_data(dashboard.url, dashboard.token, time_from, time_to)

    if endpoint_requests is None:
        return None

    endpoint_calls = []
    for request in endpoint_requests:
        # The raw endpoint call data contains a timestamp formatted
        # as "yyyy-mm-dd hh:mm:ss.micro" so we need to parse it
        time = datetime.strptime(request['time'], '%Y-%m-%d %H:%M:%S.%f')
        call = EndpointCall(
            request['endpoint'],
            request['execution_time'],
            time,
            request['version'],
            request['group_by'],
            request['ip']
        )
        endpoint_calls.append(call)

    return endpoint_calls
