import uuid
import persistent

from .aggregator import Aggregator
from .aggregator.aggregator_group import AggregatorGroup, truncate_datetime_by_granularity


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

    def aggregated_data(self, filters={}):
        """
        Returns aggregated data on this endpoint.
        :param filters: A dictionary containing property_name-value pairs to filter on. The keys are assumed to be strings.
          This is in the gist of `{'day':'2018-05-20', 'ip':'127.0.0.1'}`, thus filtering on a specific Time and IP combination.
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

    def aggregated_data_daterange(self, start_date, end_date, filters={}):
        """
        Returns the aggregated data on this endpoint over the specified daterange.
        :param start_date: A datetime object that is treated as the inclusive lower bound of the daterange.
        :param end_date: A datetime object that is treated as the exclusive upper bound of the daterange.
        :param filters: A dictionary containing property_name-value pairs to filter on. The keys are assumed to be strings.
          This is in the gist of `{'version':'1.0.1', 'ip':'127.0.0.1'}`, thus filtering on a specific Version and IP combination.
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
        return self._aggregator_group.fetch_aggregator_daterange(filters, start_date, end_date).as_dict()

    def statistic(self, statistic, filters={}):
        """
        Returns the desired statistic of this endpoint, filtered by the specified filters.
        :param statistic: A string denoting the specific statistic that should be queried.
        """ \
        f'  The following statistics are allowed:{[stat_class.field_name(stat_class) for stat_class in Aggregator.contained_statistics_classes]}.' \
        """
        :param filters: A dictionary containing property_name-value pairs to filter on. The keys are assumed to be strings.
          This is in the gist of `{'day':'2018-05-20', 'ip':'127.0.0.1'}`, thus filtering on a specific Time and IP combination.
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

    def statistic_per_timeslice(self, statistic, timeslice, timeslice_is_static, start_datetime, end_datetime, filters={}):
        f"""
        Slices up the specified datetime range (=[start_datetime, end_datetime)) into slices of the size of `timeslice`.
        For each datetime slice it computes the value of the denoted statistic and returns a dictionary containing these pairs.
        (Note that a returned datetime slice is a string: represented as the start of that slice and formatted according
         to the ISO-8601 standard.
        Filters can be applied to narrow down the search.

        :param statistic: A string denoting the specific statistic that should be queried.
        """ \
        f'  The following statistics are allowed:{[stat_class.field_name(stat_class) for stat_class in Aggregator.contained_statistics_classes]}.' \
        """
        :param timeslice: A string denoting at what granularity the indicated datetime range should be split.
          The currently supported values for this are: 'year', 'month', 'week', 'day', 'hour' and 'minute'.
        :param timeslice_is_static: A boolean denoting whether the given timeslice should be interpreted as being 'static' or 'dynamic'.
          A 'static' timeslice encompasses a preset datetime range (e.g. the month of May or the 25th day of May).
          `start_datetime` and `end_datetime` are expected to be equal to the start of their respective timeslice
          (e.g. 2000-01-01 with timeslice 'month', instead of something like 2000-01-20).
          A 'dynamic' timeslice on the other hand encompasses a set timespan (e.g. a week or a day).
          As such, timeslices whose length are not consistent (such as 'year' and 'month', excluding leap seconds) are not allowed.
        :param start_datetime: A datetime object indicating the inclusive lower bound for the datetime range to
          aggregate over.
        :param end_datetime: A datetime object indicating the exclusive upper bound for the datetime range to
         aggregate over.
        :param filters: A dictionary containing property_name-value pairs to filter on. The keys are assumed to be strings.
          This is in the gist of `{'version':'1.0.1', 'ip':'127.0.0.1'}`, thus filtering on a specific Version and IP combination.
          Defaults to an empty dictionary.

          The currently allowed filter_names are:
            - Version:
              * 'version' - e.g. '1.0.1'

            - IP:
              * 'ip' - e.g. '127.0.0.1'

            - Group-by:
              * 'group_by' - e.g. 'None'

            Note that, contrary to `aggregated_data` method, Time based filters are not allowed.
        :return: A dictionary containing datetime instances as keys and the corresponding statistic values of this endpoint as values.
        :raises ValueError: This happens when:
          - the filters are not supported by the endpoint
          - two filters of the same type are provided
          - a Time based filter is provided
          - `timeslice_is_static` is True and `start_datetime` or `end_datetime` are not at the start of their respective granularity.
        :raises KeyError: This happens when the statistic is not supported by the endpoint.
        """

        if timeslice_is_static and (start_datetime != truncate_datetime_by_granularity(start_datetime, timeslice) or
                                    end_datetime != truncate_datetime_by_granularity(end_datetime, timeslice)):
            raise ValueError(f"start_datetime and end_datetime should denote the start of their respective {timeslice}.")

        return_dict = {}
        print(f'start_datetime={start_datetime}, end_datetime={end_datetime}')
        for datetime, aggregator in self._aggregator_group.fetch_aggregators_per_timeslice(filters, timeslice,
                                                                                           start_datetime,
                                                                                           end_datetime
                                                                                           ).items():
            return_dict[datetime] = aggregator.as_dict()[statistic]

        return return_dict
