import uuid
import persistent

# from .aggregator import Aggregator
from .aggregator.aggregator_group import AggregatorGroup


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
        # self._aggregator = Aggregator(self._calls)
        self._aggregator_group = AggregatorGroup()

    def __repr__(self):
        return f'{self.__class__.__name__} id={self.id} name={self.name}'

    def get_id(self):
        return str(self.id)

    def add_endpoint_call(self, call):
        """
        Adds an EndpointCall to its internal collection of endpoint calls.
        :param call: The endpoint call to add.
        """
        self._calls.append(call)
        self._aggregator_group.add_endpoint_call(call)
        # self._aggregator.add_endpoint_call(call)

    def remove_endpoint_call(self, call):
        """
        Removes an EndpointCall from this endpoint's internal collection of endpoint calls.
        Raises a ValueError if no such call exists.
        Note: does not remove it from its aggregated dataset yet.
        :param call: The endpoint call to remove.
        """
        self._calls.remove(call)

    def set_monitored(self, is_monitored):
        self.is_monitored = is_monitored

    def aggregated_data(self):
        """
        Get aggregated data on this endpoint.
        :return: A dict containing aggregated data points.
        """
        return self._aggregator_group.fetch_aggregator({}).as_dict()

    def aggregated_data_daterange(self, start_date, end_date, granularity):
        """
        Returns the aggregated data on this dashboard over the specified daterange.
        :param start_date: A datetime object that is treated as the inclusive lower bound of the daterange.
        :param end_date: A datetime object that is treated as the inclusive upper bound of the daterange.
        :param granularity: A string denoting the granularity of the daterange.
        :return: A dictionary with all aggregated statistics and their values.
        """
        return self._aggregator_group.fetch_aggregator_inclusive_daterange({}, start_date, end_date,
                                                                           granularity).as_dict()

    def statistic(self, statistic, filters):
        """

        :param statistic:
        :param filters:
        :return:
        """
        return self._aggregator_group.fetch_aggregator(filters).as_dict()[statistic]

    def statistic_per_timeslice(self, statistic, filters, timeslice, start_datetime, end_datetime):
        """

        :param statistic:
        :param filters: A dict containing filter_name-filter_value pairs to filter on. May not contain time-based filters.
        :param timeslice:
        :param start_datetime:
        :param end_datetime:
        :return: A dictionary consisting of a datetime string (key)(formatted according to the ISO-8601 standard)
             and the corresponding statistic, over the specified datetime range.
        """
        return_dict = {}
        for datetime, aggregator in self._aggregator_group.fetch_aggregators_per_timeslice(filters, timeslice,
                                                                                           start_datetime,
                                                                                           end_datetime).items():
            return_dict[datetime] = aggregator.as_dict()[statistic]

        return return_dict
