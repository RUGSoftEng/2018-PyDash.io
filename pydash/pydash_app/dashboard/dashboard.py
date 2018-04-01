import uuid
import persistent
from datetime import datetime

from .aggregator import Aggregator
from .endpoint import Endpoint
from .endpoint_call import EndpointCall

from ..impl.fetch import get_monitor_rules, get_data

"""

Example testing code:

```
from pydash_app.dashboard.dashboard import Dashboard
from pydash_app.dashboard.endpoint import Endpoint
from pydash_app.dashboard.endpoint_call import EndpointCall
import uuid
from datetime import datetime, timedelta
d = Dashboard("http://foo.io", str(uuid.uuid4()))
e1 = Endpoint("foo", True)
e2 = Endpoint("bar", True)
d.add_endpoint(e1)
d.add_endpoint(e2)
ec1 = EndpointCall("foo", 0.5, datetime.now(), 0.1, "None", "127.0.0.1")
ec2 = EndpointCall("foo", 0.1, datetime.now(), 0.1, "None", "127.0.0.2")
ec3 = EndpointCall("bar", 0.2, datetime.now(), 0.1, "None", "127.0.0.1")
ec4 = EndpointCall("bar", 0.2, datetime.now() - timedelta(days=1), 0.1, "None", "127.0.0.1")
ec5 = EndpointCall("bar", 0.2, datetime.now() - timedelta(days=2), 0.1, "None", "127.0.0.1")
d.add_endpoint_call(ec1)
d.add_endpoint_call(ec2)
d.add_endpoint_call(ec3)
d.add_endpoint_call(ec4)
d.add_endpoint_call(ec5)
d.aggregated_data()
d.endpoints['foo'].aggregated_data()
d.endpoints['bar'].aggregated_data()
```
"""


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
        self.endpoints = dict() # name -> Endpoint
        self.last_fetch_time = None

        # TODO: implement tokens
        self.token = None

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
        Adds an endpoint call to the dashboard.
        :param endpoint_call: The endpoint call to add
        """
        self._endpoint_calls.append(endpoint_call)
        self._aggregator.add_endpoint_call(endpoint_call)

        if endpoint_call.endpoint in self.endpoints:
            self.endpoints[endpoint_call.endpoint].add_endpoint_call(endpoint_call)

    def aggregated_data(self):
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
