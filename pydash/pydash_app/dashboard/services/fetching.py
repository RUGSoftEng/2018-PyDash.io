from functools import partial
from datetime import datetime, timedelta, timezone

import json
import requests.exceptions
import jwt

import flask_monitoring_dashboard_client
from pydash_app.dashboard.endpoint import Endpoint
from pydash_app.dashboard.endpoint_call import EndpointCall
from pydash_app.dashboard.entity import DashboardState
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
    initialization_states = (
        DashboardState.not_initialized,
        DashboardState.initialized_endpoints,
        DashboardState.initialize_endpoints_failure,
        DashboardState.initialized_endpoint_calls,
        DashboardState.initialize_endpoint_calls_failure
    )
    for dashboard in dashboard_repository.all():
        if dashboard.state in initialization_states:
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

    logger.info(f'INSIDE FETCH FUNCTION: {dashboard_id}')

    fetch_and_add_endpoint_calls(dashboard)

    logger.info(f'{len(dashboard.endpoints)} endpoints found')
    logger.info(f'{len(dashboard._endpoint_calls)} endpoint calls')

    dashboard_repository.update(dashboard)

    logger.info(f"Dashboard {dashboard_id} updated")


def fetch_and_update_historic_dashboard_info(dashboard_id):
    """
    Updates the dashboard with the historic EndpointCall information that is fetched from the Dashboard's remote location.
    """
    dashboard = dashboard_repository.find(dashboard_id)

    logger.info(f'INSIDE INITIAL FETCHING FUNCTION: {dashboard_id}')

    fetch_and_add_endpoints(dashboard)
    fetch_and_add_historic_endpoint_calls(dashboard)

    logger.info(f'{len(dashboard.endpoints)} endpoints found')
    logger.info(f'{len(dashboard._endpoint_calls)} historical endpoint calls')

    dashboard_repository.update(dashboard)


# Endpoints


def fetch_and_add_endpoints(dashboard):
    """
    For a given dashboard, initialize it with the endpoints it has registered.
    Note that this will not add endpoint call data.
    :param dashboard: The dashboard to initialize with endpoints.
    """

    # Only run this function if no endpoints have been added yet
    if dashboard.state != DashboardState.not_initialized:
        logger.warning(f'Tried to add endpoints from a wrong state: {dashboard.state} for dashboard: {dashboard}')
        return

    try:
        details = flask_monitoring_dashboard_client.get_details(dashboard.url)
    except requests.exceptions.ConnectionError as e:
        logger.error(f'Connection error in fetch_and_add_endpoints while initializing: {e}\n'
                     f'from dashboard: {dashboard}')
        dashboard.state = DashboardState.initialize_endpoints_failure
        dashboard.error = "Could not connect to the remote application while initializing endpoint information."
        return
    except requests.exceptions.Timeout as e:
        logger.error(f'Timeout in fetch_and_add_endpoints while initializing: {e}\n'
                     f'from dashboard: {dashboard}')
        dashboard.state = DashboardState.initialize_endpoints_failure
        dashboard.error = "The connection to the remote application timed out while initializing endpoint information."
        return
    except requests.exceptions.HTTPError as e:
        logger.error(f'HTTP error in fetch_and_add_endpoints while initializing: {e}\n'
                     f'from dashboard: {dashboard}')
        dashboard.state = DashboardState.initialize_endpoints_failure
        dashboard.error = "Could not connect to the remote application while initializing endpoint information."
        return
    except json.JSONDecodeError as e:
        logger.error(f'JSON decode error in fetch_and_add_endpoints while initializing: {e}\n')
        dashboard.state = DashboardState.initialize_endpoints_failure
        dashboard.error = "Could not read the remote dashboard's details while initializing endpoint information."
        return
    except Exception as e:
        logger.error(f'Unexpected error in fetch_and_add_endpoints while initializing: {e}\n'
                     f'from dashboard: {dashboard}')
        dashboard.state = DashboardState.initialize_endpoints_failure
        dashboard.error = str(e)
        return

    try:
        version = details['dashboard-version']
    except KeyError:
        try:
            version = details['version']
        except KeyError:
            version = '?'

        logger.error(f'Unsupported dashboard version: {details}')
        dashboard.state = DashboardState.initialize_endpoints_failure
        dashboard.error = f"You are running an unsupported version of Flask-MonitoringDashboard ({version} < 1.12.0)."
        return

    try:
        endpoints = _fetch_endpoints(dashboard)
    except requests.exceptions.ConnectionError as e:
        logger.error(f'Connection error in fetch_and_add_endpoints while fetching: {e}\n'
                     f'from dashboard: {dashboard}')
        dashboard.state = DashboardState.initialize_endpoints_failure
        dashboard.error = "Could not connect to the remote application while fetching endpoint information."
        return
    except requests.exceptions.Timeout as e:
        logger.error(f'Timeout in fetch_and_add_endpoints while fetching: {e}\n'
                     f'from dashboard: {dashboard}')
        dashboard.state = DashboardState.initialize_endpoints_failure
        dashboard.error = "The connection to the remote application timed out while fetching endpoint information."
        return
    except requests.exceptions.HTTPError as e:
        logger.error(f'HTTP error in fetch_and_add_endpoints while fetching: {e}\n'
                     f'from dashboard: {dashboard}')
        dashboard.state = DashboardState.initialize_endpoints_failure
        dashboard.error = "Could not connect to the remote application while fetching endpoint information."
        return
    except jwt.DecodeError as e:
        logger.error(f'JWT decode error in fetch_and_add_endpoints while fetching: {e}\n'
                     f'from dashboard: {dashboard}')
        dashboard.state = DashboardState.initialize_endpoints_failure
        dashboard.error = "Could not read the remote dashboard's endpoint information."
        return
    except KeyError as e:
        logger.error(f'Key error in fetch_and_add_endpoints while fetching: {e}\n'
                     f'from dashboard: {dashboard}')
        dashboard.state = DashboardState.initialize_endpoints_failure
        dashboard.error = "Could not read the remote dashboard's endpoint information."
        return
    except json.JSONDecodeError as e:
        logger.error(f'JSON decode error in fetch_and_add_endpoints while fetching: {e}\n')
        dashboard.state = DashboardState.initialize_endpoints_failure
        dashboard.error = "Could not read the remote dashboard's endpoint information."
        return
    except Exception as e:
        logger.error(f'Unexpected error in fetch_and_add_endpoints while fetching: {e}\n'
                     f'from dashboard: {dashboard}')
        dashboard.state = DashboardState.initialize_endpoints_failure
        dashboard.error = str(e)
        return

    for endpoint in endpoints:
        dashboard.add_endpoint(endpoint)

    dashboard.state = DashboardState.initialized_endpoints
    dashboard.error = None


def _fetch_endpoints(dashboard):
    """
    Fetches and returns a list of `Endpoint`s in the given dashboard.
    :param dashboard: The dashboard for which to fetch endpoints.
    :return: A list of `Endpoint`s for the dashboard.
    """

    # Note: exceptions raised by flask_monitoring_dashboard_client.get_monitor_rules
    # are simply propagated upwards, since this is not the best place
    # to handle them; this function is meant to be more or less "pure"

    monitor_rules = flask_monitoring_dashboard_client.get_monitor_rules(
        dashboard.url, dashboard.token)

    return [
        Endpoint(rule['endpoint'], rule['monitor']) for rule in monitor_rules
    ]


# EndpointCalls


def fetch_and_add_historic_endpoint_calls(dashboard):
    """
    For a given dashboard, retrieve all historical endpoint calls and add them to it.
    :param dashboard: The dashboard to initialize with historical data.
    """

    # Only run this function if no periodic fetching of latest information has happened yet:
    if dashboard.state != DashboardState.initialized_endpoints:
        logger.warning(
            f'Tried to add historic endpoint calls from a wrong state: {dashboard.state} for dashboard: {dashboard}')
        return

    try:
        details = flask_monitoring_dashboard_client.get_details(dashboard.url)
    except requests.exceptions.ConnectionError as e:
        logger.error(f'Connection error happened while initializing EndpointCalls: {e}\n'
                     f'for dashboard: {dashboard}')
        dashboard.state = DashboardState.initialize_endpoint_calls_failure
        dashboard.error = "Could not connect to the remote application while initializing historical data."
        return
    except requests.exceptions.Timeout as e:
        logger.error(f'Timeout happened while initializing EndpointCalls: {e}\n'
                     f'for dashboard: {dashboard}')
        dashboard.state = DashboardState.initialize_endpoint_calls_failure
        dashboard.error = "The connection to the remote application timed out while initializing historical data."
        return
    except requests.exceptions.HTTPError as e:
        logger.error(f'HTTP error happened while initializing EndpointCalls: {e}\n'
                     f'for dashboard: {dashboard}')
        dashboard.state = DashboardState.initialize_endpoint_calls_failure
        dashboard.error = "Could not connect to the remote application while initializing historical data."
        return
    except json.JSONDecodeError as e:
        logger.error(f'JSON decode error happened while initializing EndpointCalls: {e}\n'
                     f'for dashboard: {dashboard}')
        dashboard.state = DashboardState.initialize_endpoint_calls_failure
        dashboard.error = "Could not read the remote dashboard's details while initializing historical data."
        return
    except Exception as e:
        logger.error(f'Unexpected error happened while initializing EndpointCalls: {e}\n'
                     f'from dashboard: {dashboard}')
        dashboard.state = DashboardState.initialize_endpoint_calls_failure
        dashboard.error = str(e)
        return

    try:
        first_request = int(details['first-request'])
    except KeyError:
        logger.error(f'Dashboard details do not contain date of first request: {details}')
        dashboard.state = DashboardState.initialize_endpoint_calls_failure
        dashboard.error = "The dashboard's details do not contain the date of the first request."
        return
    except ValueError:
        logger.error(f"Dashboard details date of first request is not a timestamp: {details['first_request']}")
        dashboard.state = DashboardState.initialize_endpoint_calls_failure
        dashboard.error = "The dashboard's time of the first request is not a timestamp."
        return

    if first_request == -1:
        error_text = f'There are no historic endpoint calls yet'
        logger.error(error_text)
        dashboard.state = DashboardState.initialize_endpoint_calls_failure
        dashboard.error = "Your application has no recorded request data yet."
        return

    # TODO: for now we start fetching simply one second before the first request because the lower bound
    # TODO: of _fetch_endpoint_calls is exclusive
    start_time = datetime.fromtimestamp(first_request - 1, tz=timezone.utc)
    current_time = datetime.now(timezone.utc)

    while start_time < current_time:
        # TODO: for now historical data is pulled in chunks of 1 hour (hardcoded)
        end_time = start_time + timedelta(hours=1)

        if end_time > current_time:
            end_time = current_time

        try:
            endpoint_calls = _fetch_endpoint_calls(dashboard, start_time, end_time)
        except requests.exceptions.ConnectionError as e:
            logger.error(f'Connection error happened while fetching historical EndpointCalls: {e}\n'
                         f'for dashboard: {dashboard}')
            dashboard.state = DashboardState.initialize_endpoint_calls_failure
            dashboard.error = "Could not connect to the remote application while fetching historical data."
            return
        except requests.exceptions.Timeout as e:
            logger.error(f'Timeout happened while fetching EndpointCalls: {e}\n'
                         f'for dashboard: {dashboard}')
            dashboard.state = DashboardState.initialize_endpoint_calls_failure
            dashboard.error = "The connection to the remote application timed out while fetching historical data."
            return
        except requests.exceptions.HTTPError as e:
            logger.error(f'HTTP error happened while fetching historical EndpointCalls: {e}\n'
                         f'for dashboard: {dashboard}')
            dashboard.state = DashboardState.initialize_endpoint_calls_failure
            dashboard.error = "Could not connect to the remote application while fetching historical data."
            return
        except jwt.DecodeError as e:
            logger.error(f'JWT decode error happened while fetching historical EndpointCalls: {e}\n'
                         f'for dashboard {dashboard}')
            dashboard.state = DashboardState.initialize_endpoint_calls_failure
            dashboard.error = "Could not read the remote dashboard's historical data (is your security code valid?)."
            return
        except KeyError as e:
            logger.error(f'Key error happened while fetching historical EndpointCalls: {e}\n'
                         f'for dashboard: {dashboard}')
            dashboard.state = DashboardState.initialize_endpoint_calls_failure
            dashboard.error = "Could not read the remote dashboard's historical data."
            return
        except json.JSONDecodeError as e:
            logger.error(f'JSON decode error happened while fetching historical EndpointCalls: {e}\n'
                         f'for dashboard: {dashboard}')
            dashboard.state = DashboardState.initialize_endpoint_calls_failure
            dashboard.error = "Could not read the remote dashboard's historical data."
            return
        except Exception as e:
            logger.error(f'Unexpected error happened while fetching historical EndpointCalls: {e}\n'
                         f'from dashboard: {dashboard}')
            dashboard.state = DashboardState.initialize_endpoints_failure
            dashboard.error = str(e)
            return

        for call in endpoint_calls:
            dashboard.add_endpoint_call(call)
            dashboard.last_fetch_time = call.time

        start_time = end_time

    dashboard.state = DashboardState.initialized_endpoint_calls
    dashboard.error = None


def fetch_and_add_endpoint_calls(dashboard):
    """
    Retrieve the latest endpoint calls of the given dashboard and add them to it.
    :param dashboard: The dashboard for which to update endpoint calls.
    """

    logger.info(f"Updating endpoint calls for dashboard: {dashboard}")

    # Only run this function if historic fetching has happened:
    # - in the initialized_endpoint_calls state, we have just successfully fetched historic endpoint calls;
    # - in the fetched_endpoint_calls state, we have just successfully fetched new endpoint calls;
    # - in the fetch_endpoint_calls_failure state, we have failed to get the latest endpoint calls, so we will retry.
    allowed_states = (
        DashboardState.initialized_endpoint_calls,
        DashboardState.fetched_endpoint_calls,
        DashboardState.fetch_endpoint_calls_failure
    )
    if dashboard.state not in allowed_states:
        logger.warning(
            f'Tried to add new endpoint calls from a wrong state: {dashboard.state} for dashboard: {dashboard}')
        return

    try:
        new_calls = _fetch_endpoint_calls(
            dashboard, time_from=dashboard.last_fetch_time)
    except requests.exceptions.ConnectionError as e:
        logger.error(f'Connection error in fetch_and_add_endpoint_calls: {e}\n'
                     f'from dashboard {dashboard}')
        dashboard.state = DashboardState.fetch_endpoint_calls_failure
        dashboard.error = "Could not connect to the remote application while fetching new data."
        return
    except requests.exceptions.Timeout as e:
        logger.error(f'Timeout in fetch_and_add_endpoint_calls: {e}\n'
                     f'for dashboard: {dashboard}')
        dashboard.state = DashboardState.initialize_endpoint_calls_failure
        dashboard.error = "The connection to the remote application timed out while fetching new data."
        return
    except requests.exceptions.HTTPError as e:
        logger.error(f'HTTP error in fetch_and_add_endpoint_calls: {e}\n'
                     f'from dashboard {dashboard}')
        dashboard.state = DashboardState.fetch_endpoint_calls_failure
        dashboard.error = "Could not connect to the remote application while fetching new data."
        return
    except jwt.DecodeError as e:
        logger.error(f'JWT decode error in fetch_and_add_endpoint_calls: {e}\n'
                     f'from dashboard {dashboard}')
        dashboard.state = DashboardState.fetch_endpoint_calls_failure
        dashboard.error = "Could not read the remote dashboard's data (is your security code valid?)."
        return
    except KeyError as e:
        logger.error(f'Key error in fetch_and_add_endpoint_calls: {e}\n'
                     f'from dashboard {dashboard}')
        dashboard.state = DashboardState.fetch_endpoint_calls_failure
        dashboard.error = "Could not read the remote dashboard's new data."
        return
    except json.JSONDecodeError as e:
        logger.error(f'JSON decode error in fetch_and_add_endpoint_calls: {e}\n')
        dashboard.state = DashboardState.fetch_endpoint_calls_failure
        dashboard.error = "Could not read the remote dashboard's new data."
        return
    except ValueError as e:
        logger.error(f'Value error in fetch_and_add_endpoint_calls: {e}\n')
        dashboard.state = DashboardState.fetch_endpoint_calls_failure
        dashboard.error = "Could not read the remote dashboard's new data."
        return
    except Exception as e:
        logger.error(f'Unexpected error in fetch_and_add_endpoint_calls: {e}\n'
                     f'from dashboard: {dashboard}')
        dashboard.state = DashboardState.initialize_endpoints_failure
        dashboard.error = str(e)
        return

    if not new_calls:
        logger.info(f'No new calls for dashboard: {dashboard}')
        return

    logger.info(f'New endpoint calls: {new_calls}')

    for call in new_calls:
        dashboard.add_endpoint_call(call)

    dashboard.last_fetch_time = new_calls[-1].time
    dashboard.state = DashboardState.fetched_endpoint_calls
    dashboard.error = None

    logger.info(f'Saved to database: dashboard {dashboard}')


def _fetch_endpoint_calls(dashboard, time_from=None, time_to=None):
    """
    Fetches and returns a list of `EndpointCall`s for the given dashboard.
    :param dashboard: The dashboard for which to fetch endpoint calls.
    :param time_from: An operiodic_tasksional datetime indicating only data since that moment should be returned.
    :param time_to: An operiodic_tasksional datetime indicating only data up to that point should be returned.
    :return: A list of `EndpointCall`s containing the endpoint call data for this dashboard.
    """

    # Note: exceptions raised by flask_monitoring_dashboard_client.get_data
    # are simply propagated upwards, since this is not the best place
    # to handle them; this function is meant to be more or less "pure"

    endpoint_requests = flask_monitoring_dashboard_client.get_data(
        dashboard.url, dashboard.token, time_from, time_to)

    endpoint_calls = []
    for request in endpoint_requests:
        # The raw endpoint call data contains a timestamp formatted
        # as "yyyy-mm-dd hh:mm:ss.micro" so we need to parse it
        try:
            time = datetime.strptime(request['time'], '%Y-%m-%d %H:%M:%S.%f')
        except ValueError:
            logger.error(f'Failed to parse the time of an endpoint call: {request}\n'
                         f'from dashboard: {dashboard}')
            raise

        time.replace(tzinfo=timezone.utc)

        call = EndpointCall(request['endpoint'], request['execution_time'],
                            time, request['version'], request['group_by'],
                            request['ip'])
        endpoint_calls.append(call)

    return endpoint_calls
