import uuid
import persistent

from .aggregator import Aggregator
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
        :raises ValueError: If `call` is not in this endpoint's internal collection of endpoint calls.
        """
        self._calls.remove(call)

    def set_monitored(self, is_monitored):
        self.is_monitored = is_monitored

    def aggregated_data(self, filters={}):
        """
        Returns aggregated data on this endpoint.
        :param filters: A dictionary containing property_name-value pairs to filter on. The keys are assumed to be strings.
          This is in the gist of `{'day':'2018-05-20', 'ip':'127.0.0.1'}`
          Defaults to an empty dictionary.

          The currently allowed filter_names are:
            - Time:
              * 'year'   - e.g. '2018'
              * 'month'  - e.g. '2018-05'
              * 'week'   - e.g. '2018-W17'
              * 'day'    - e.g. '2018-05-20'
              * 'hour'   - e.g. '2018-05-20T20'
              * 'minute' - e.g. '2018-05-20T20-10'
            Note that for Time filter-values, the formatting is crucial.

            - Version:
              * 'version' - e.g. '1.0.1'

            - IP:
              * 'ip' - e.g. '127.0.0.1'

            - Group-by:
              * 'group_by' - e.g. 'None'

        :return: A dict containing aggregated data points.
        """
        return self._aggregator_group.fetch_aggregator(filters).as_dict()

    def aggregated_data_daterange(self, start_date, end_date, granularity, filters={}):
        """
        Returns the aggregated data on this endpoint over the specified daterange.
        :param start_date: A datetime object that is treated as the inclusive lower bound of the daterange.
        :param end_date: A datetime object that is treated as the inclusive upper bound of the daterange.
        :param granularity: A string denoting the granularity of the daterange.
        :param filters: A dictionary containing property_name-value pairs to filter on. The keys are assumed to be strings.
          This is in the gist of `{'day':'2018-05-20', 'ip':'127.0.0.1'}`
          Defaults to an empty dictionary.

          The currently allowed filter_names are:
            - Version:
              * 'version' - e.g. '1.0.1'

            - IP:
              * 'ip' - e.g. '127.0.0.1'

            - Group-by:
              * 'group_by' - e.g. 'None'

            Note that, contrary to `aggregated_data` method, Time based filters are not allowed.

        :return: A dictionary with all aggregated statistics and their values.
        """
        return self._aggregator_group.fetch_aggregator_inclusive_daterange(filters, start_date, end_date,
                                                                           granularity).as_dict()

    def statistic(self, statistic, filters={}):
        """
        Returns the desired statistic of this endpoint, filtered by the specified filters.
        :param statistic: A string denoting the specific statistic that should be queried.
        """ \
        f'  The following filters are allowed:{[stat_class.field_name(stat_class) for stat_class in Aggregator.contained_statistics_classes]}.' \
        """
        :param filters: A dictionary containing property_name-value pairs to filter on. The keys are assumed to be strings.
          This is in the gist of `{'day':'2018-05-20', 'ip':'127.0.0.1'}`
          Defaults to an empty dictionary.

          The currently allowed filter_names are:
            - Time:
              * 'year'   - e.g. '2018'
              * 'month'  - e.g. '2018-05'
              * 'week'   - e.g. '2018-W17'
              * 'day'    - e.g. '2018-05-20'
              * 'hour'   - e.g. '2018-05-20T20'
              * 'minute' - e.g. '2018-05-20T20-10'
            Note that for Time filter-values, the formatting is crucial.

            - Version:
              * 'version' - e.g. '1.0.1'

            - IP:
              * 'ip' - e.g. '127.0.0.1'

            - Group-by:
              * 'group_by' - e.g. 'None'

        :return: The desired statistic of this endpoint.
        :raises ValueError: This happens when the filters are not supported by the endpoint, or when two filters of
          the same type are provided.
        :raises KeyError: This happens when the statistic is not supported by the endpoint.
        """
        return self._aggregator_group.fetch_aggregator(filters).as_dict()[statistic]

    def statistic_per_timeslice(self, statistic, timeslice, start_datetime, end_datetime, filters={}):
        f"""
        Slices up the specified datetime range (=[start_datetime, end_datetime]) by chunks of the size of `timeslice`.
        For each datetime_slice it computes the value of the denoted statistic and returns a dictionary containing these pairs.
        (Note that a returned datetime_slice is a string: represented as the start of that slice and formatted according
         to the ISO-8601 standard.
        Filters can be applied to narrow down the search.

        :param statistic: A string denoting the specific statistic that should be queried.
        """ \
        f'  The following filters are allowed:{[stat_class.field_name(stat_class) for stat_class in Aggregator.contained_statistics_classes]}.' \
        """
        :param timeslice: A string denoting at what granularity the indicated datetime range should be split.
          The currently supported values for this are: 'year', 'month', 'week', 'day', 'hour' and 'minute'.
        :param start_datetime: A datetime object indicating the inclusive lower bound for the datetime range to
         aggregate over.
        :param end_datetime:  A datetime object indicating the inclusive upper bound for the datetime range to
         aggregate over.
        :param filters: A dictionary containing property_name-value pairs to filter on. The keys are assumed to be strings.
          This is in the gist of `{'day':'2018-05-20', 'ip':'127.0.0.1'}`
          Defaults to an empty dictionary.

          The currently allowed filter_names are:
            - Version:
              * 'version' - e.g. '1.0.1'

            - IP:
              * 'ip' - e.g. '127.0.0.1'

            - Group-by:
              * 'group_by' - e.g. 'None'

            Note that, contrary to `statistic` method, Time based filters are not allowed.
        :return: The desired statistic of this endpoint.
        :raises ValueError: This happens when the filters are not supported by the endpoint, or when two filters of
          the same type are provided, or when a Time based filter is provided.
        :raises KeyError: This happens when the statistic is not supported by the endpoint.
        """
        return_dict = {}
        for datetime, aggregator in self._aggregator_group.fetch_aggregators_per_timeslice(filters, timeslice,
                                                                                           start_datetime,
                                                                                           end_datetime).items():
            return_dict[datetime] = aggregator.as_dict()[statistic]

        return return_dict
