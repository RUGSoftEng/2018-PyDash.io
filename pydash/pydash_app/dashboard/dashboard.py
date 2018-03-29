
import uuid
import persistent

from .aggregator import Aggregator


class Dashboard(persistent.Persistent):
    """
    The Dashboard entity knows about:
    - Its own properties (id, url, user_id, endpoints, endpoint_calls and last_fetch_time)
    - The functionalities for Dashboard interactions with information from elsewhere.

    It does not contain information on how to persistently store/load a dashboard.
    This task is handled by the `dashboard_repository`.
    """

    def __init__(self, url, user_id):
        if not isinstance(url, str) or not isinstance(user_id, str):
            raise TypeError("Dashboard expects both url and user_id to be strings.")

        self.id = uuid.uuid4()
        self.url = url
        self.user_id = uuid.UUID(user_id)
        self.endpoints = []
        self.last_fetch_time = None

        self._endpoint_calls = []  # list of unfiltered endpoint calls, for use with an aggregator.
        self._aggregator = Aggregator(self._endpoint_calls)

    def __repr__(self):
        return f'<{self.__class__.__name__} id={self.id} url={self.url} endpoints={self.endpoints}>'

    def get_id(self):
        return str(self.id)

    def add_endpoint(self, endpoint):
        """
        Adds an endpoint to this dashboard's internal collection of endpoints.
        :param endpoint:  The endpoint to add, expects an Endpoint object.
        """
        self.endpoints.append(endpoint)

    def remove_endpoint(self, endpoint):
        """
        Removes an endpoint from this dashboard's internal collection of endpoints.

        Raises a ValueError if no such endpoint exists.
        :param endpoint: The endpoint to remove.
        """
        # TODO: perhaps remove all relevant endpoint calls from endpoint_calls? Discuss with team.
        # TODO: THIS IS POST-MVP
        self.endpoints.remove(endpoint)

    def add_endpoint_call(self, endpoint_call):
        """
        Adds an endpoint call to the dashboard.
        :param endpoint_call: The endpoint call to add
        """
        self._endpoint_calls.append(endpoint_call)
        self._aggregator.add_endpoint_call(endpoint_call)
        
        # Quick and dirty fix to add endpoint call to endpoint
        for endpoint in self.endpoints:
            if endpoint.name == endpoint_call.endpoint:
                endpoint.add_call(endpoint_call)
                break

    def get_aggregated_data(self):
        """
        Returns aggregated data on this dashboard.
        :return: A dict containing aggregated data points.
        """
        return self._aggregator.as_dict()

    # Required because `multi_indexed_collection` puts dashboards in a set,
    #  that needs to order its keys for fast lookup.
    # Because the IDs are unchanging integer values, use that.
    def __lt__(self, other):
        return self.id < other.id
