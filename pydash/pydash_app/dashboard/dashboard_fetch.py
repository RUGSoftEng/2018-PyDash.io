from datetime import datetime, timedelta

from ..impl.fetch import get_monitor_rules, get_data, get_details
from .endpoint import Endpoint
from .endpoint_call import EndpointCall
from .dashboard_repository import update as update_dashboard


def fetch_endpoints(dashboard):
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

    fetch_start_time = datetime.utcnow() - timedelta(minutes=1)

    if dashboard.last_fetch_time is None:
        return

    new_calls = _fetch_endpoint_calls(dashboard, dashboard.last_fetch_time)
    for call in new_calls:
        dashboard.add_endpoint_call(call)

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
