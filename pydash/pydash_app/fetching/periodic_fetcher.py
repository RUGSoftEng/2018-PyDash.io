import pydash_app.impl.periodic_tasks as pt
import datetime
from functools import partial
from pydash_app.dashboard.dashboard_fetch import initialize_endpoint_calls, update_endpoint_calls, fetch_endpoints

"""

"""


pt.start_default_scheduler()  # Perhaps move this to pydash.__init__.py to ensure the task scheduler is always running and make sure that we don't start it again when importing this module.


def initialise_dashboard(dashboard, interval, scheduler):
    """
    Initialise a dashboard's (remote) endpoints and add them to the scheduler, with the given interval.
    :param dashboard: The Dashboard to initialise.
    :param interval: The interval at which the endpoints should be fetched. Defaults to 1 hour.
    :param scheduler: The scheduler to add the fetch calls to.
     Defaults to the default TaskScheduler provided in the pydash_app.impl.periodic_tasks package.
    """
    endpoints = fetch_endpoints(dashboard)
    initialize_endpoint_calls(dashboard)

    for endpoint in endpoints:
        _add_endpoint_to_fetch_from(dashboard, endpoint, interval, scheduler)


def update_dashboard(dashboard, interval, scheduler, override_previous_endpoint_interval=True):
    """
    Update a dashboard from its remote endpoints and add fetching them to the scheduler, with the given interval.
    :param dashboard: The Dashboard to update.
    :param interval: The interval at which the endpoints should be fetched. Defaults to 1 hour.
    :param scheduler: The scheduler to add the fetch calls to.
     Defaults to the default TaskScheduler provided in the pydash_app.impl.periodic_tasks package.
    :param override_previous_endpoint_interval: A Boolean to indicate whether the user wishes to override the interval
     of all other endpoint-fetching connected to this dashboard. Defaults to True.
    """
    old_endpoints = dict(dashboard.endpoints)  # Make sure that new_endpoints is not the same object as old_endpoints.
    new_endpoints = fetch_endpoints(dashboard)  # Relies on fetch_endpoints to return a dict of endpoints.

    # Add new endpoints and override
    for endpoint in new_endpoints:
        if override_previous_endpoint_interval or endpoint not in old_endpoints:
            _add_endpoint_to_fetch_from(dashboard, new_endpoints[endpoint], interval, scheduler)

    # Remove obsolete endpoints
    for endpoint in old_endpoints:
        if endpoint not in new_endpoints:
            _remove_endpoint_to_fetch_from(dashboard, old_endpoints[endpoint])
            dashboard.remove_endpoint(old_endpoints[endpoint])


def _add_endpoint_to_fetch_from(dashboard, endpoint, interval=datetime.timedelta(hours=1), scheduler=pt.default_task_scheduler):
    """
    Adds the fetching of data from `endpoint` of `dashboard` to the given scheduler.
    Defaults to the default scheduler that is provided in the pydash_app.impl.periodic_tasks package.
    :param dashboard: The Dashboard this Endpoint belongs to.
    :param endpoint: The Endpoint in question.
    :param interval: The Datetime.Timedelta object indicating the interval of the fetching, starting from this moment in time.
     Defaults to 1 hour.
    :param scheduler: The TaskScheduler we want to add this Endpoint-fetching to.
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
