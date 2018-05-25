from collections import defaultdict
from itertools import chain, combinations
import persistent
from datetime import datetime, timedelta
from copy import copy

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
PartitionByMinute = AggregatorPartitionFun('minute', 'time', partition_by_minute_fun)


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
        self._p_changed = True # ZODB mark object as changed


    def fetch_aggregator(self, filter_dict):
        """
        Filters the internal collection of aggregators and returns the right one depending on filter_dict.
        :param filter_dict: A dictionary containing property_name-value pairs to filter on.
          This is in the gist of `{'day':'2018-05-20', 'ip':'127.0.0.1'}`

          The current filter_names are:
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
              * 'group_by' - e.g. None

          Note that when providing two filters of the same type, a ValueError is raised.

        :return: An Aggregator instance that contains the right aggregated data for this query.
          Note that if an invalid value is given, a new (and empty) Aggregator is returned, due to the lazy addition.
        """
        try:
            partition = self.partition_names[frozenset(filter_dict.keys())]
        except KeyError:
            # TODO: discern what exactly goes wrong higher up in the callback chain.
            raise ValueError("Bad input value: input filter type is not supported,"
                             " input filter-value not formatted correctly,"
                             " or multiple input filters of the same type.")
        return self.partitions[partition][frozenset(filter_dict.values())]

    def fetch_aggregator_daterange(self, filters, datetime_begin, datetime_end):
        """
        Fetches an aggregator over the entire provided datetime range. Note that filters may not contain time-based
        properties.
        :param filters: A dictionary that contains property_name-value pairs to filter on.
          This is in the gist of {'ip': '127.0.0.1', 'version': '1.0.1'}
          For the complete set of possible filters, see AggregatorGroup.fetch_aggregator.
        :param datetime_begin: A datetime object indicating the inclusive lower bound for the datetime range to
         aggregate over.
        :param datetime_end:  A datetime object indicating the exclusive upper bound for the datetime range to
         aggregate over.
        :return: An Aggregator object that contains the aggregated data over the entirety of the specified datetime
         range.
        """
        for key in filters.keys:
            if key in ['year', 'month', 'week', 'day', 'hour', 'minute']:
                raise ValueError('filters may not contain time-based properties')

        date_chunks = chop_date_range_into_chunks(datetime_begin, datetime_end)
        aggregator = None

        filters_cpy = copy(filters)
        for day in date_chunks['day']:
            filters_cpy['day'] = f'{day.year}-{day.month}-{day.day}'
            aggregator += self.fetch_aggregator(filters_cpy)

        filters_cpy = copy(filters)
        for hour in date_chunks['hour']:
            filters_cpy['hour'] = f'{hour.year}-{hour.month}-{hour.day}T{hour.hour}'
            aggregator += self.fetch_aggregator(filters_cpy)

        filters_cpy = copy(filters)
        for minute in date_chunks['minute']:
            filters_cpy['minute'] = f'{minute.year}-{minute.month}-{minute.day}T{minute.hour}-{minute.minute}'

        return aggregator


def chop_date_range_into_chunks(datetime_begin, datetime_end):
    """
    Chops the given datetime range into chunks of full days, hours and minutes.
    :param datetime_begin: A datetime object that indicates the inclusive lower bound of the datetime range.
    :param datetime_end: A datetime object that indicates the exclusive upper bound of the datetime range.
    :return: A dict with the keys "days", "hours" and "minutes", where the values are lists of corresponding datetime
     granulates.
    """

    chunks = {
              "day": [],
              "hour": [],
              "minute": []
             }

    days, (complete_l, complete_r) = chop_date_range_into_days(datetime_begin, datetime_end)
    chunks["day"] = days
    if complete_l and complete_r:
        return chunks

    if not days:
        hours, (complete_l, complete_r) = chop_date_range_into_hours(datetime_begin, datetime_end)
    else:
        if not complete_l:
            hours_l, (complete_l, _) = chop_date_range_into_hours(datetime_begin,
                                                                  datetime(year=days[0].year,
                                                                           month=days[0].month,
                                                                           day=days[0].day
                                                                           )
                                                                  )
        else:
            hours_l = []
        if not complete_r:
            hours_r, (_, complete_r) = chop_date_range_into_hours(datetime(year=datetime_end.year,
                                                                           month=datetime_end.month,
                                                                           day=datetime_end.day
                                                                           ),
                                                                  datetime_end
                                                                  )
        else:
            hours_r = []
        hours = hours_l + hours_r
    chunks["hour"] = hours
    if complete_l and complete_r:
        return chunks

    if not hours:
        minutes = chop_date_range_into_minutes(datetime_begin, datetime_end)
    else:
        if not complete_l:
            minutes_l = chop_date_range_into_minutes(datetime_begin,
                                                     datetime(year=hours[0].year,
                                                              month=hours[0].month,
                                                              day=hours[0].day,
                                                              hour=hours[0].hour
                                                              )
                                                     )
        else:
            minutes_l = []
        if not complete_r:
            minutes_r = chop_date_range_into_minutes(datetime(year=datetime_end.year,
                                                              month=datetime_end.month,
                                                              day=datetime_end.day,
                                                              hour=datetime_end.hour
                                                              ),
                                                     datetime_end
                                                     )
        else:
            minutes_r = []
        minutes = minutes_l + minutes_r
    chunks["minute"] = minutes
    return chunks


def chop_date_range_into_days(datetime_begin, datetime_end):
    """
    Returns a range of days (datetimes) that are fully within the given date range.
    :param datetime_begin: a datetime object that indicates the inclusive lower bound of the desired date-range
    :param datetime_end: a datetime object that indicates the exclusive upper bound of the desired date-range
    :return: An ordered list of datetime objects containing the days that are fully within the given range,
        as well as a tuple containing whether the left part and the right part of the date range have been consumed completely.
    """
    if datetime_begin > datetime_end:
        raise ValueError("date_begin cannot be larger than date_end")
    range_begin = datetime_begin.day
    range_end = datetime_end.day
    complete_l = True
    complete_r = True
    if datetime_begin.hour != 0 or datetime_begin.minute != 0:
        range_begin += 1
        complete_l = False
    if datetime_end.hour != 0 or datetime_end.minute != 0:
        complete_r = False
    range_begin = datetime(datetime_begin.year, datetime_begin.month, range_begin)
    range_end   = datetime(datetime_end.year, datetime_end.month, range_end)
    num_days    = (range_end - range_begin).days
    return [range_begin + day * timedelta(days=1) for day in range(num_days)], (complete_l, complete_r)


def chop_date_range_into_hours(datetime_begin, datetime_end):
    """
    Returns a range of hours (datetimes) that are fully within the given date range.
    :param datetime_begin: a datetime object that indicates the inclusive lower bound of the desired date-range
    :param datetime_end: a datetime object that indicates the exclusive upper bound of the desired date-range
    :return: An ordered list of datetime objects containing the hours that are fully within the given range,
        as well as a tuple containing whether the left part and the right part of the date range have been consumed completely.
    """
    if datetime_begin > datetime_end:
        raise ValueError("date_begin cannot be larger than date_end")
    range_begin = datetime_begin.hour
    range_end = datetime_end.hour
    complete_l = True
    complete_r = True

    if datetime_begin.minute != 0:
        range_begin += 1
        complete_l = False
    if datetime_end.minute != 0:
        complete_r = False

    range_begin = datetime(datetime_begin.year, datetime_begin.month, datetime_begin.day, range_begin)
    range_end   = datetime(datetime_end.year, datetime_end.month, datetime_end.day, range_end)
    num_hours   = int((range_end - range_begin).total_seconds() / 3600)
    return [range_begin + hour * timedelta(seconds=3600) for hour in range(num_hours)], (complete_l, complete_r)


def chop_date_range_into_minutes(datetime_begin, datetime_end):
    """
    Returns a range of minutes (datetimes) that are fully within the given date range.
    :param datetime_begin: a datetime object that indicates the inclusive lower bound of the desired date-range
    :param datetime_end: a datetime object that indicates the exclusive upper bound of the desired date-range
    :return: An ordered list of datetime objects containing the minutes that are fully within the given range.
    Note that this function will not take any lower kind of granularity into account than datetime.minute,
      so the input `datetime(..., minute=6, second=20)` will be treated as `datetime(..., minute=6, second=0)`, etc.
    """
    if datetime_begin > datetime_end:
        raise ValueError("date_begin cannot be larger than date_end")
    num_minutes = int((datetime_end - datetime_begin).total_seconds() / 60)
    return [datetime_begin + minute * timedelta(seconds=60) for minute in range(num_minutes)]
