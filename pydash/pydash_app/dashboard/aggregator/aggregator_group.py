from collections import defaultdict
from itertools import chain, combinations
import persistent
from datetime import datetime

from . import Aggregator

def powerset_generator(i):
    for subset in chain.from_iterable(combinations(i, r) for r in range(len(i)+1)):
        yield list(subset)


class AggregatorPartitionFun:
    def __init__(self, field_name, category, fun):
        self.field_name = field_name
        self.fun = fun
        self.category = category

    def __call__(self, endpoint_call):
        return self.fun(endpoint_call)

    def __repr__(self):
        return f"<{self.__class__.__name__} field_name={self.field_name} category={self.category} >"


def partition_by_year_fun(endpoint_call):
    return endpoint_call.time.strftime("%Y")
PartitionByYear = AggregatorPartitionFun('year', 'time', partition_by_year_fun)


def partition_by_month_fun(endpoint_call):
    return endpoint_call.time.strftime("%Y-%m")
PartitionByMonth = AggregatorPartitionFun('month', 'time', partition_by_month_fun)


def partition_by_week_fun(endpoint_call):
    return endpoint_call.time.strftime("%Y-W%W")
PartitionByWeek = AggregatorPartitionFun('week', 'time', partition_by_week_fun)


def partition_by_day_fun(endpoint_call):
    return endpoint_call.time.strftime("%Y-%m-%d")
PartitionByDay = AggregatorPartitionFun('day', 'time', partition_by_day_fun)


def partition_by_hour_fun(endpoint_call):
    return endpoint_call.time.strftime("%Y-%m-%dT%H")
PartitionByHour = AggregatorPartitionFun('hour', 'time', partition_by_hour_fun)

def partition_by_minute_fun(endpoint_call):
    return endpoint_call.time.strftime("%Y-%m-%dT%H-%M")
PartitionByHour = AggregatorPartitionFun('minute', 'time', partition_by_minute_fun)


def partition_by_version_fun(endpoint_call):
    return endpoint_call.version
PartitionByVersion = AggregatorPartitionFun('version', 'version', partition_by_version_fun)


def partition_by_ip_fun(endpoint_call):
    return endpoint_call.ip
PartitionByIP = AggregatorPartitionFun('ip', 'ip', partition_by_ip_fun)


def partition_by_group_by_fun(endpoint_call):
    return endpoint_call.group_by
PartitionByGroupBy = AggregatorPartitionFun('group_by', 'group_by', partition_by_group_by_fun)


def remove_duplicate_categories(partition_funs):
    categories = set()
    for partition_fun in partition_funs:
        if partition_fun.category in categories:
            next
        else:
            categories.add(partition_fun.category)
            yield partition_fun


def calc_endpoint_call_identifier(partition, endpoint_call):
    return frozenset(partition_fun(endpoint_call) for partition_fun in partition)


def partition_field_names(partition):
    for partition_fun in partition:
        yield partition_fun.field_name


class AggregatorGroup(persistent.Persistent):
    """
    Maintains a powerset of dicts of aggregators,
    such that we can filter based on:
    - time
    - IP
    - FMD's group_by
    - etc.

    Involved usage example:
    >>> from datetime import datetime
    >>> from pydash_app.dashboard.endpoint_call import EndpointCall
    >>> from pydash_app.dashboard.aggregator.aggregator_group import AggregatorGroup
    >>> ag = AggregatorGroup()
    >>> ec1 = EndpointCall("foo", 0.5, datetime.strptime("2018-04-25 15:29:23", "%Y-%m-%d %H:%M:%S"), "0.1", "None", "127.0.0.1")
    >>> ec2 = EndpointCall("foo", 0.5, datetime.strptime("2018-04-26 15:29:23", "%Y-%m-%d %H:%M:%S"), "0.1", "None", "127.0.0.1")
    >>> ec3 = EndpointCall("foo", 0.5, datetime.strptime("2018-04-25 15:29:23", "%Y-%m-%d %H:%M:%S"), "0.1", "None", "127.0.0.2")
    >>> ag.add_endpoint_call(ec1)
    >>> ag.add_endpoint_call(ec2)
    >>> ag.add_endpoint_call(ec3)
    >>> a_day = ag.fetch_aggregator({'day':'2018-04-25'})
    >>> # Filter by day
    ... a_day.as_dict()
    {'total_visits': 2, 'total_execution_time': 1.0, 'average_execution_time': 0.5, 'visits_per_day': {'2018-04-25': 2}, 'visits_per_ip': {'127.0.0.1': 1, '127.0.0.2': 1}, 'unique_visitors': 2, 'unique_visitors_per_day': {'2018-04-25': 2}, 'fastest_measured_execution_time': 0.5, 'fastest_quartile_execution_time': 0.5, 'median_execution_time': 0.5, 'slowest_quartile_execution_time': 0.5, 'ninetieth_percentile_execution_time': 0.5, 'ninety-ninth_percentile_execution_time': 0.5, 'slowest_measured_execution_time': 0.5}
    >>> # Filter by week
    ... a_week = ag.fetch_aggregator({'week':'2018-W17'})
    >>> a_week.as_dict()
    {'total_visits': 3, 'total_execution_time': 1.5, 'average_execution_time': 0.5, 'visits_per_day': {'2018-04-25': 2, '2018-04-26': 1}, 'visits_per_ip': {'127.0.0.1': 2, '127.0.0.2': 1}, 'unique_visitors': 2, 'unique_visitors_per_day': {'2018-04-25': 2, '2018-04-26': 1}, 'fastest_measured_execution_time': 0.5, 'fastest_quartile_execution_time': 0.5, 'median_execution_time': 0.5, 'slowest_quartile_execution_time': 0.5, 'ninetieth_percentile_execution_time': 0.5, 'ninety-ninth_percentile_execution_time': 0.5, 'slowest_measured_execution_time': 0.5}
    >>> # Filter by day and ip
    ... a_day_ip = ag.fetch_aggregator({'day':'2018-04-25', 'ip':'127.0.0.1'})
    >>> a_day_ip.as_dict()
    {'total_visits': 1, 'total_execution_time': 0.5, 'average_execution_time': 0.5, 'visits_per_day': {'2018-04-25': 1}, 'visits_per_ip': {'127.0.0.1': 1}, 'unique_visitors': 1, 'unique_visitors_per_day': {'2018-04-25': 1}, 'fastest_measured_execution_time': 0.5, 'fastest_quartile_execution_time': 0.5, 'median_execution_time': 0.5, 'slowest_quartile_execution_time': 0.5, 'ninetieth_percentile_execution_time': 0.5, 'ninety-ninth_percentile_execution_time': 0.5, 'slowest_measured_execution_time': 0.5}
    >>> # No filtering (all endpoint calls are included in this aggregator)
    ... a_all = ag.fetch_aggregator({})
    >>> a_all.as_dict()
    {'total_visits': 3, 'total_execution_time': 1.5, 'average_execution_time': 0.5, 'visits_per_day': {'2018-04-25': 2, '2018-04-26': 1}, 'visits_per_ip': {'127.0.0.1': 2, '127.0.0.2': 1}, 'unique_visitors': 2, 'unique_visitors_per_day': {'2018-04-25': 2, '2018-04-26': 1}, 'fastest_measured_execution_time': 0.5, 'fastest_quartile_execution_time': 0.5, 'median_execution_time': 0.5, 'slowest_quartile_execution_time': 0.5, 'ninetieth_percentile_execution_time': 0.5, 'ninety-ninth_percentile_execution_time': 0.5, 'slowest_measured_execution_time': 0.5}

    """

    partition_funs = [
        PartitionByYear,
        PartitionByMonth,
        PartitionByWeek,
        PartitionByDay,
        PartitionByHour,
        PartitionByMinute,
        PartitionByGroupBy,
        PartitionByIP,
        PartitionByVersion,
    ]

    """ Note to our internal dev team:
    To add more partitions to filter on, a corresponding AggregatorPartitionFun class instance should be created
    (together with its corresponding 'partition_by_' function) and added to the `partition_funs` list above.
    """

    partition_powerset = powerset_generator(partition_funs)
    partitions_set = frozenset(frozenset(remove_duplicate_categories(elem)) for elem in partition_powerset)

    def __init__(self, endpoint_calls=[]):
        """
        Sets up the aggregator group that will lazily create new Aggregators when needed.
        :param endpoint_calls: An iterable collection of endpoint calls to seed the AggregatorGroup with.
        """
        self.partitions = dict()  # frozenset(partitions) -> defaultdict(Aggregator)
        self.partition_names = dict()  # frozenset(partition field names) -> frozenset(partitions)
        for elem in self.partitions_set:
            self.partitions[elem] = defaultdict(Aggregator)  # frozenset(partition field names) -> Aggregator
            self.partition_names[frozenset(partition_field_names(elem))] = elem
        for endpoint_call in endpoint_calls:
            self.add_endpoint_call(endpoint_call)

    def add_endpoint_call(self, endpoint_call):
        """Adds the given endpoint call to the right aggregators within the group."""
        for (partition, aggregator_dict) in self.partitions.items():
            endpoint_call_identifier = calc_endpoint_call_identifier(partition, endpoint_call)
            aggregator_dict[endpoint_call_identifier].add_endpoint_call(endpoint_call)

    def fetch_aggregator(self, partition_field_names):
        """
        Filters the internal collection of aggregators and returns the right one depending on partition_field_names.
        :param partition_field_names: A dictionary containing filter_name-value pairs to filter on.
          This is in the gist of `{'day':'2018-05-20', 'ip':'127.0.0.1'}`

          The current filter_names are:
            - Time:
              * 'year' - e.g. '2018'
              * 'week' - e.g. '2018-W17'
              * 'day'  - e.g. '2018-05-20'
              * 'hour' - e.g. '2018-05-20T20'

            Note that for Time filter-values, the formatting is crucial.

            - Version:
              * 'version' - e.g. '1.0.1'

            - IP:
              * 'ip' - e.g. '127.0.0.1'

            - Group-by:
              * 'group_by' - e.g. None

          Note that when providing two filters of the same type, a

        :return: An Aggregator instance that contains the right aggregated data for this query.
          Note that if an invalid value is given, a new (and empty) Aggregator is returned, due to the lazy addition.
        """
        try:
            partition = self.partition_names[frozenset(partition_field_names.keys())]
        except KeyError:
            # TODO: discern what exactly goes wrong higher up in the callback chain.
            raise ValueError("Bad input value: input filter type is not supported,"
                             " input filter-value not formatted correctly,"
                             " or multiple input filters of the same type.")
        return self.partitions[partition][frozenset(partition_field_names.values())]

def fetch_aggregator_daterange(filters, date_begin, date_end):





def chop_date_range_into_chunks(date_begin, date_end):
    years = chop_date_range_into_years(date_begin, date_end)
    weeks = get_weeks_from_beginning_of_year() + get_weeks_until_end_of_year()
    days = []
    hours = []

def chop_date_range_into_years(datetime_begin, datetime_end):
    if datetime_begin > datetime_end:
        raise ValueError("date_begin cannot be larger than date_end")

    if datetime_begin == datetime(year=datetime_begin.year, month=0, day=0, hour=0):
        range_begin = datetime_begin.year
    else:
        range_begin = datetime_begin.year + 1
    if datetime_end == datetime(year=datetime_end.year, month=0, day=0, hour=0):
        range_end = datetime_end.year - 1
    else:
        range_end = datetime_end.year

    return [year for year in range(range_begin, range_end)]

def get_weeks_until_end_of_year(datetime_begin):
    return [week for week in range(datetime_begin, 53)]

def get_weeks_from_beginning_of_year(datetime_end):
    return [week for week in range(datetime_end)]