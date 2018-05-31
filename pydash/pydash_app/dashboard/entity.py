"""

Involved usage example:

>>> from pydash_app.dashboard.entity import Dashboard
>>> from pydash_app.user.entity import User
>>> from pydash_app.dashboard.endpoint import Endpoint
>>> from pydash_app.dashboard.endpoint_call import EndpointCall
>>> import uuid
>>> from datetime import datetime, timedelta
>>> user = User("Gandalf", "pass")
>>> d = Dashboard("http://foo.io", str(uuid.uuid4()), str(user.id))
>>> e1 = Endpoint("foo", True)
>>> e2 = Endpoint("bar", True)
>>> d.add_endpoint(e1)
>>> d.add_endpoint(e2)
>>> ec1 = EndpointCall("foo", 0.5, datetime.strptime("2018-04-25 15:29:23", "%Y-%m-%d %H:%M:%S"), "0.1", "None", "127.0.0.1")
>>> ec2 = EndpointCall("foo", 0.1, datetime.strptime("2018-04-25 15:29:23", "%Y-%m-%d %H:%M:%S"), "0.1", "None", "127.0.0.2")
>>> ec3 = EndpointCall("bar", 0.2, datetime.strptime("2018-04-25 15:29:23", "%Y-%m-%d %H:%M:%S"), "0.1", "None", "127.0.0.1")
>>> ec4 = EndpointCall("bar", 0.2, datetime.strptime("2018-04-25 15:29:23", "%Y-%m-%d %H:%M:%S") - timedelta(days=1), "0.1", "None", "127.0.0.1")
>>> ec5 = EndpointCall("bar", 0.2, datetime.strptime("2018-04-25 15:29:23", "%Y-%m-%d %H:%M:%S") - timedelta(days=2), "0.1", "None", "127.0.0.1")
>>> d.add_endpoint_call(ec1)
>>> d.add_endpoint_call(ec2)
>>> d.add_endpoint_call(ec3)
>>> d.add_endpoint_call(ec4)
>>> d.add_endpoint_call(ec5)
>>> d.aggregated_data()
{'total_visits': 5, 'total_execution_time': 1.2, 'average_execution_time': 0.24, 'visits_per_day': {'2018-04-25': 3, '2018-04-24': 1, '2018-04-23': 1}, 'visits_per_ip': {'127.0.0.1': 4, '127.0.0.2': 1}, 'unique_visitors': 2, 'unique_visitors_per_day': {'2018-04-25': 2, '2018-04-24': 1, '2018-04-23': 1}, 'fastest_measured_execution_time': 0.1, 'fastest_quartile_execution_time': 0.14, 'median_execution_time': 0.2, 'slowest_quartile_execution_time': 0.39, 'ninetieth_percentile_execution_time': 0.5, 'ninety-ninth_percentile_execution_time': 0.5, 'slowest_measured_execution_time': 0.5}
>>> d.endpoints['foo'].aggregated_data()
{'total_visits': 2, 'total_execution_time': 0.6, 'average_execution_time': 0.3, 'visits_per_day': {'2018-04-25': 2}, 'visits_per_ip': {'127.0.0.1': 1, '127.0.0.2': 1}, 'unique_visitors': 2, 'unique_visitors_per_day': {'2018-04-25': 2}, 'fastest_measured_execution_time': 0.1, 'fastest_quartile_execution_time': 0.1, 'median_execution_time': 0.3, 'slowest_quartile_execution_time': 0.5, 'ninetieth_percentile_execution_time': 0.5, 'ninety-ninth_percentile_execution_time': 0.5, 'slowest_measured_execution_time': 0.5}
>>> d.endpoints['bar'].aggregated_data()
{'total_visits': 3, 'total_execution_time': 0.6, 'average_execution_time': 0.2, 'visits_per_day': {'2018-04-25': 1, '2018-04-24': 1, '2018-04-23': 1}, 'visits_per_ip': {'127.0.0.1': 3}, 'unique_visitors': 1, 'unique_visitors_per_day': {'2018-04-25': 1, '2018-04-24': 1, '2018-04-23': 1}, 'fastest_measured_execution_time': 0.2, 'fastest_quartile_execution_time': 0.2, 'median_execution_time': 0.2, 'slowest_quartile_execution_time': 0.2, 'ninetieth_percentile_execution_time': 0.2, 'ninety-ninth_percentile_execution_time': 0.2, 'slowest_measured_execution_time': 0.2}

"""

import uuid
import persistent
import datetime
from enum import Enum

from pydash_app.dashboard.endpoint import Endpoint
from pydash_app.dashboard.aggregator.aggregator_group import AggregatorGroup
from pydash_app.dashboard.downtime import DowntimeLog

class DashboardState(Enum):
    """
    The DashboardState enum indicates the state in which a Dashboard can remain, regarding remote fetching:

    - not_initialized indicates the dashboard is newly created and not initialized with Endpoints and
      historic EndpointCalls;

    - initialized_endpoints indicates the dashboard has successfully initialized Endpoints,
      but not yet historical EndpointCalls;
    - initialize_endpoints_failure indicates something went wrong while initializing Endpoints, which means
      initialization of Endpoints needs to be retried;

    - initialized_endpoint_calls indicates the dashboard has successfully initialized historical EndpointCalls,
      and can start fetching new EndpointCalls in a periodic task;
    - initialize_endpoint_calls_failure indicates something went wrong while initializing historical EndpointCalls,
      which means this needs to be retried;

    - fetched_endpoint_calls indicates last time new EndpointCalls were fetched, it was done successfully;
    - fetch_endpoint_calls_failure indicates something went wrong while fetching new EndpointCalls,
      which means this needs to be retried.
    """
    not_initialized = 0

    initialized_endpoints = 10
    initialize_endpoints_failure = 11

    initialized_endpoint_calls = 20
    initialize_endpoint_calls_failure = 21

    fetched_endpoint_calls = 30
    fetch_endpoint_calls_failure = 31


class Dashboard(persistent.Persistent):
    """
    The Dashboard entity knows about:
    - Its own properties (id, url, user_id, endpoints, endpoint_calls and last_fetch_time)
    - The functionalities for Dashboard interactions with information from elsewhere.

    It does not contain information on how to persistently store/load a dashboard.
    This task is handled by the `dashboard_repository`.
    """

    def __init__(self, url, token, user_id, name=None, monitor_downtime=False):
        if not isinstance(url, str) or not isinstance(token, str):
            raise TypeError("Dashboard expects both url and token to be strings.")

        if name is not None and not isinstance(name, str):
            raise TypeError("Dashboard expects name to be a string.")

        if not isinstance(monitor_downtime, bool):
            raise TypeError("Dashboard expects monitor_downtime to be a string.")

        # Make sure integers and strings are allowed as well.
        if not isinstance(user_id, uuid.UUID):
            user_id = uuid.UUID(user_id)

        self.id = uuid.uuid4()
        self.url = url
        self.user_id = user_id
        self.token = token
        self.name = name

        self.endpoints = dict()  # name -> Endpoint

        self.last_fetch_time = None
        self.state = DashboardState.not_initialized
        self.error = None

        self._endpoint_calls = []  # list of unfiltered endpoint calls, for use with an aggregator.
        self._aggregator_group = AggregatorGroup()

        self.monitor_downtime = monitor_downtime
        self._downtime_log = DowntimeLog()

    def __repr__(self):
        return f'<{self.__class__.__name__} id={self.id} url={self.url}>'

    def get_id(self):
        return str(self.id)

    def add_endpoint(self, endpoint):
        """
        Adds an endpoint to this dashboard's internal collection of endpoints.
        :param endpoint:  The endpoint to add, expects an Endpoint object.
        """
        self.endpoints[endpoint.name] = endpoint

    def remove_endpoint(self, endpoint):
        """
        Removes an endpoint from this dashboard's internal collection of endpoints.

        Raises a ValueError if no such endpoint exists.
        :param endpoint: The endpoint to remove.
        """
        # TODO: perhaps remove all relevant endpoint calls from endpoint_calls? Discuss with team.
        # TODO: THIS IS POST-MVP
        # TODO: Is this function required at all?
        del self.endpoints[endpoint.name]

    def add_endpoint_call(self, endpoint_call):
        """
        Adds an endpoint call to the dashboard. Will register the corresponding endpoint to the dashboard if this has
         not been done yet.
        :param endpoint_call: The endpoint call to add
        """
        # Adds endpoint to list of endpoints if it has not been registered yet.
        if endpoint_call.endpoint not in self.endpoints:  # Note: this is possible, because the names are the keys.
            self.add_endpoint(Endpoint(endpoint_call.endpoint, True))
        self.endpoints[endpoint_call.endpoint].add_endpoint_call(endpoint_call)

        self._endpoint_calls.append(endpoint_call)
        self._aggregator_group.add_endpoint_call(endpoint_call)

    def aggregated_data(self):
        """
        Returns aggregated data on this dashboard.
        :return: A dict containing aggregated data points.
        """
        return self._aggregator_group.fetch_aggregator({}).as_dict()

    def add_ping_result(self, is_up, ping_datetime=datetime.datetime.now(tz=datetime.timezone.utc)):
        """
        Adds the result of a ping request to the dashboard.
        :param is_up: Whether the dashboard's web service is up.
        :param ping_datetime: When the ping took place (approximately); defaults to the current time in UTC.
        """
        self._downtime_log.add_ping_result(is_up, ping_datetime)

    def get_downtime_data(
            self,
            start=datetime.datetime.now(tz=datetime.timezone.utc).date() - datetime.timedelta(days=90),
            end=datetime.datetime.now(tz=datetime.timezone.utc).date()):
        """
        Returns a dict containing this dashboard's downtime data for a given date range.
        :param start: The start date (exclusive; defaults to 90 days before the current date).
        :param end: The end date (inclusive; defaults to the current date).
        :return: A dictionary containing the dashboard's downtime data in the given date range.
        """
        return {
            'downtime_intervals': self._downtime_log.get_downtime_intervals(start, end),
            'total_downtimes': self._downtime_log.get_total_downtimes(start, end),
            'downtime_percentage': self._downtime_log.get_downtime_percentage(start, end)
        }

    # Required because `multi_indexed_collection` puts dashboards in a set,
    #  that needs to order its keys for fast lookup.
    # Because the IDs are unchanging integer values, use that.
    def __lt__(self, other):
        return self.id < other.id
