import uuid
import persistent

from .aggregator import Aggregator


class Endpoint(persistent.Persistent):
    """
    The Endpoint entity knows about:
    - Its own properties
    - The functionalities for Endpoint interactions with information from elsewhere.

    It does not contain information on how to persistently store/load an endpoint,
    as currently endpoints only exist in combination with dashboard objects.
    If endpoints were to exist on their own, the `endpoint_repository` would handle their persistence.
    """

    def __init__(self, name, is_monitored):
        if not isinstance(name, str):
            raise TypeError('Endpoint expects name to be a string.')

        self.id = uuid.uuid4()
        self.name = name
        self.is_monitored = is_monitored

        self._calls = []
        self._aggregator = Aggregator(self._calls)

    def __repr__(self):
        return f'{self.__class__.__name__} id={self.id} name={self.name}'

    def get_id(self):
        return str(self.id)

    def add_call(self, call):
        """
        Adds a call to its internal collection of endpoint calls.
        :param call: The endpoint call to add.
        """
        self._calls.append(call)
        self._aggregator.add_endpoint_call(call)

    def remove_call(self, call):
        """
        Removes a call from this endpoint's internal collection of endpoint calls.
        Raises a ValueError if no such call exists.
        :param call: The endpoint call to remove.
        """
        self._calls.remove(call)

    def set_monitored(self, is_monitored):
        self.is_monitored = is_monitored

    def get_aggregated_data(self):
        """
        Get aggregated data on this endpoint.
        :return: A dict containing aggregated data points.
        """
        return self._aggregator.as_dict()
