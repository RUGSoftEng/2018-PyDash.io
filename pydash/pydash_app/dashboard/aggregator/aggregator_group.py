from collections import defaultdict
from itertools import chain, combinations
import persistent
from datetime import datetime, timedelta
import calendar
from copy import copy, deepcopy
from dtrange import dtrange
from more_itertools import peekable


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


datetime_formats = {'year': '%Y'}
datetime_formats['month'] = datetime_formats['year'] + '-%m'
datetime_formats['week'] = datetime_formats['year'] + '-W%W'
datetime_formats['day'] = datetime_formats['month'] + '-%d'
datetime_formats['hour'] = datetime_formats['day'] + 'T%H'
datetime_formats['minute'] = datetime_formats['hour'] + '-%M'

# allowed_timeslices = ['year', 'month', 'week_static', 'week_dynamic', 'day_static', 'day_dynamic', 'hour_static',
#                       'hour_dynamic', 'minute_static', 'minute_dynamic']

dynamic_timeslices = ['week', 'day', 'hour', 'minute']
static_timeslices = ['year', 'month', 'week', 'day', 'hour', 'minute']

allowed_timeslices = ['year', 'month', 'week', 'day', 'hour', 'minute']


# granularity_to_timedelta_convertor = {'week_static': timedelta(weeks=1), 'week_dynamic': timedelta(weeks=1),
#                                       'day_static': timedelta(days=1), 'day_dynamic': timedelta(days=1),
#                                       'hour_static': timedelta(hours=1), 'hour_dynamic': timedelta(hours=1),
#                                       'minute_static': timedelta(minutes=1), 'minute_dynamic': timedelta(minutes=1)
#                                       }
#
# granularity_to_timedelta_convertor_original = {'week': timedelta(weeks=1), 'week_dynamic': timedelta(weeks=1),
#                                       'week_static': timedelta(weeks=1), 'day': timedelta(days=1),
#                                       'hour': timedelta(hours=1), 'minute': timedelta(minutes=1)
#                                       }
#
# granularity_to_timedelta_convertor_with_is_static = {'week': timedelta(weeks=1), 'day': timedelta()}


# def inclusive_to_exclusive_datetime_adaptor(end_date, granularity):
#     """This is for the Gregorian calendar only. Note that one should not use this to add time, due to possible
#     truncation of dates. (e.g. input 2000-1-30 and 'month' would result in 2000-2-29."""
#     if granularity in granularity_to_timedelta_convertor.keys():
#         return end_date + granularity_to_timedelta_convertor[granularity]
#     else:
#         year = end_date.year
#         month = end_date.month
#         day = end_date.day
#         hour = end_date.hour
#         minute = end_date.minute
#
#         if granularity in ['year', 'month']:
#             if granularity == 'year':
#                 next_year = year+1
#                 max_month_day = calendar.monthrange(next_year, month)
#                 if day > max_month_day:
#                     return datetime(next_year, month, max_month_day, hour, minute)
#                 else:
#                     return datetime(next_year, month, day, hour, minute)
#             else:
#                 next_year = year + int((month+1)/12)
#                 next_month = (month+1) % 12
#                 max_next_month_day = calendar.monthrange(next_year, next_month)[1]
#                 if day > max_next_month_day:
#                     return datetime(next_year, next_month, max_next_month_day, hour, minute)
#                 else:
#                     return datetime(next_year, next_month, day, hour, minute)
#         else:
#             raise ValueError(f'Granularity {granularity} is not supported.')


def truncate_datetime_by_granularity(datetime_value, granularity):
    if granularity == 'year':
        return datetime(datetime_value.year, 1, 1)
    if granularity == 'month':
        return datetime(datetime_value.year, datetime_value.month, 1)
    if granularity == 'week':  # This is assuming 'week' is meant as a static week in the year (e.g. 2018W23)
        # using 1 as week day in order to have %W be used in calculations. Also Python week days are rather counter-intuitive,
        # as 1 is the beginning of the week (monday) and this loops around to 0 as the end of the week (sunday).
        return datetime.strptime(f'{datetime_value.year}W{int(datetime_value.strftime("%W"))}-1', '%YW%W-%w')
    if granularity == 'day':
        return datetime(datetime_value.year, datetime_value.month, datetime_value.day)
    if granularity == 'hour':
        return datetime(datetime_value.year, datetime_value.month, datetime_value.day, datetime_value.hour)
    if granularity == 'minute':
        return datetime(datetime_value.year, datetime_value.month, datetime_value.day, datetime_value.hour, datetime_value.minute)
    raise ValueError(f'Invalid granularity {granularity}')


def partition_by_year_fun(endpoint_call):
    return endpoint_call.time.strftime(datetime_formats['year'])
PartitionByYear = AggregatorPartitionFun('year', 'time', partition_by_year_fun)


def partition_by_month_fun(endpoint_call):
    return endpoint_call.time.strftime(datetime_formats['month'])
PartitionByMonth = AggregatorPartitionFun('month', 'time', partition_by_month_fun)


def partition_by_week_fun(endpoint_call):
    return endpoint_call.time.strftime(datetime_formats['week'])
PartitionByWeek = AggregatorPartitionFun('week', 'time', partition_by_week_fun)


def partition_by_day_fun(endpoint_call):
    return endpoint_call.time.strftime(datetime_formats['day'])
PartitionByDay = AggregatorPartitionFun('day', 'time', partition_by_day_fun)


def partition_by_hour_fun(endpoint_call):
    return endpoint_call.time.strftime(datetime_formats['hour'])
PartitionByHour = AggregatorPartitionFun('hour', 'time', partition_by_hour_fun)

def partition_by_minute_fun(endpoint_call):
    return endpoint_call.time.strftime(datetime_formats['minute'])
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
    >>>
    >>> # Filter by day
    ... a_day = ag.fetch_aggregator({'day':'2018-04-25'})
    >>> a_day.as_dict()['total_visits'] == 2
    True
    >>>
    >>> # Filter by week
    ... a_week = ag.fetch_aggregator({'week':'2018-W17'})
    >>> a_week.as_dict()['total_visits'] == 3
    True
    >>>
    >>> # Filter by day and ip
    ... a_day_ip = ag.fetch_aggregator({'day':'2018-04-25', 'ip':'127.0.0.1'})
    >>> a_day_ip.as_dict()['total_visits'] == 1
    True
    >>>
    >>> # No filtering (all endpoint calls are included in this aggregator)
    ... a_all = ag.fetch_aggregator({})
    >>> a_all.as_dict()['total_visits'] == 3
    True
    >>>
    >>> # Filter over a datetime range
    ... start_datetime = datetime(ec1.time.year, ec1.time.month, ec1.time.day)
    >>> end_datetime = datetime(ec2.time.year, ec2.time.month, ec2.time.day + 1)
    >>> a_all2 = ag.fetch_aggregator_daterange({}, start_datetime, end_datetime)
    >>> a_all2.as_dict()['total_visits'] == 3
    True
    >>> a_all.as_dict() == a_all2.as_dict()
    True

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

    def fetch_aggregator(self, filter_dict={}):
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
              * 'group_by' - e.g. 'None'

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
        Fetches an aggregator over the entire provided datetime range.
        :param filters: A dictionary that contains property_name-value pairs to filter on.
          This is in the gist of {'ip': '127.0.0.1', 'version': '1.0.1'}
          For the complete set of possible filters, see AggregatorGroup.fetch_aggregator.
          Note: may not contain time-based filters, for obvious reasons.
        :param datetime_begin: A datetime object indicating the inclusive lower bound for the datetime range to
         aggregate over.
        :param datetime_end:  A datetime object indicating the exclusive upper bound for the datetime range to
         aggregate over.
        :return: An Aggregator object that contains the aggregated data over the entirety of the specified datetime
         range.
        """

        for key in filters.keys():
            if key in allowed_timeslices:
                raise ValueError('filters may not contain time-based properties')
        print(f'datetime_begin={datetime_begin}, datetime_end={datetime_end}')
        date_chunks = _chop_date_range_into_chunks(datetime_begin, datetime_end)
        aggregator = Aggregator()
        for key, value in date_chunks.items():
            filters_cpy = deepcopy(filters)
            for datetime in value:
                filters_cpy[key] = datetime.strftime(datetime_formats[key])
                aggregator += self.fetch_aggregator(filters_cpy)

        return aggregator

    # def fetch_aggregator_inclusive_daterange(self, filters, datetime_begin, datetime_end, granularity):
    #     """
    #     Fetches an aggregator over the entire provided datetime range.
    #     :param filters: A dictionary that contains property_name-value pairs to filter on.
    #       This is in the gist of {'ip': '127.0.0.1', 'version': '1.0.1'}
    #       For the complete set of possible filters, see AggregatorGroup.fetch_aggregator.
    #       Note: May not contain time-based filters, for obvious reasons.
    #     :param datetime_begin: A datetime object indicating the inclusive lower bound for the datetime range to
    #      aggregate over.
    #     :param datetime_end:  A datetime object indicating the inclusive upper bound for the datetime range to
    #      aggregate over.
    #     :param granularity: A string denoting the granularity of the daterange. This can be one of the following:
    #                         'year', 'month', 'week', 'day', 'hour', 'minute'.
    #     :return: An Aggregator object that contains the aggregated data over the entirety of the specified datetime
    #      range.
    #     """
    #     datetime_begin = truncate_datetime_by_granularity(datetime_begin, granularity)
    #     datetime_end = truncate_datetime_by_granularity(datetime_end, granularity)
    #     return self.fetch_aggregator_daterange(filters, datetime_begin, inclusive_to_exclusive_datetime_adaptor(datetime_end, granularity))

    def fetch_aggregators_per_timeslice(self, filters, timeslice, start_datetime, end_datetime):
        """
        These datetimes are treated as inclusive boundaries of a datetime range (e.g. [start_datetime, end_datetime].
        Assumes start_datetime and end_datetime are both from utc.
        :param filters: A dictionary that contains property_name-value pairs to filter on.
          This is in the gist of {'ip': '127.0.0.1', 'version': '1.0.1'}
          For the complete set of possible filters, see AggregatorGroup.fetch_aggregator.
          Note: May not contain time-based filters, for obvious reasons.
        :param timeslice: A string denoting at what granularity the indicated datetime range should be split.
          The currently supported values for this are: 'year', 'month', 'week', 'day', 'hour' and 'minute'.
        :param start_datetime: A datetime object indicating the inclusive lower bound for the datetime range to
          aggregate over.
        :param end_datetime: A datetime object indicating the exclusive upper bound for the datetime range to
          aggregate over.
        :return: A list of tuples consisting of a datetime instances and the corresponding aggregator,
          over the specified datetime range.
        """
        statistics_aggregators = {}

        def datetime_range(start, stop, step, unit):
            """Note: datetime_range has an exclusive upper-bound (stop)."""
            def add_time(datetime_value, step, unit):
                # We cannot simply multiply by step here, since each step is not necessarily equal.
                # (i.e. not every month has the same amount of days or there might be a leap year)
                for _ in range(step):
                    datetime_value += convert_unit_to_timedelta(datetime_value, unit)
                return datetime_value

            current_datetime_value = start
            while current_datetime_value < stop:
                yield current_datetime_value
                current_datetime_value = add_time(current_datetime_value, step, unit)

        daterange = peekable(datetime_range(start_datetime, end_datetime, 1, timeslice))
        for datetime_value in daterange:
            # print(f'datetime_value={datetime_value}, next_datetime_value={next_datetime_value}')
            try:
                next_datetime_value = daterange.peek()
            except StopIteration:
                next_datetime_value = end_datetime
            statistic_aggregator = self.fetch_aggregator_daterange(filters, datetime_value, next_datetime_value)
            statistics_aggregators[datetime_value] = statistic_aggregator

        return statistics_aggregators


def convert_unit_to_timedelta(datetime_value, unit):
    if unit == 'year':
        if calendar.isleap(datetime_value.year):
            return timedelta(days=366)
        else:
            return timedelta(days=365)
    if unit == 'month':
        return timedelta(days=calendar.monthrange(datetime_value.year, datetime_value.month)[1])
    if unit == 'week':
        return timedelta(weeks=1)
    if unit == 'day':
        return timedelta(days=1)
    if unit == 'hour':
        return timedelta(hours=1)
    if unit == 'minute':
        return timedelta(minutes=1)


def _chop_date_range_into_chunks(datetime_begin, datetime_end):
    """
    Chops the given datetime range into chunks of full days, hours and minutes. Does account for leap seconds.
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

    days, (complete_l, complete_r) = _chop_date_range_into_days(datetime_begin, datetime_end)
    chunks["day"] = days
    if complete_l and complete_r:
        return chunks

    if not days:
        hours, (complete_l, complete_r) = _chop_date_range_into_hours(datetime_begin, datetime_end)
    else:
        if not complete_l:
            hours_l, (complete_l, _) = _chop_date_range_into_hours(datetime_begin,
                                                                   datetime(year=days[0].year,
                                                                            month=days[0].month,
                                                                            day=days[0].day,
                                                                            )
                                                                   )
        else:
            hours_l = []
        if not complete_r:
            hours_r, (_, complete_r) = _chop_date_range_into_hours(datetime(year=datetime_end.year,
                                                                            month=datetime_end.month,
                                                                            day=datetime_end.day,
                                                                            ),
                                                                   datetime_end
                                                                   )
        else:
            hours_r = []
        hours = hours_l + hours_r
    chunks["hour"] = hours
    if complete_l and complete_r:
        return chunks

    if not days and not hours:
        minutes = _chop_date_range_into_minutes(datetime_begin, datetime_end)
    else:
        if not complete_l:
            minutes_l = _chop_date_range_into_minutes(datetime_begin,
                                                      datetime(year=hours[0].year,
                                                               month=hours[0].month,
                                                               day=hours[0].day,
                                                               hour=hours[0].hour,
                                                               )
                                                      )
        else:
            minutes_l = []
        if not complete_r:
            minutes_r = _chop_date_range_into_minutes(datetime(year=datetime_end.year,
                                                               month=datetime_end.month,
                                                               day=datetime_end.day,
                                                               hour=datetime_end.hour,
                                                               ),
                                                      datetime_end
                                                      )
        else:
            minutes_r = []
        minutes = minutes_l + minutes_r
    chunks["minute"] = minutes
    return chunks


def _chop_date_range_into_days(datetime_begin, datetime_end):
    """
    Returns a range of days (datetimes) that are fully within the given date range.
    :param datetime_begin: a datetime object that indicates the inclusive lower bound of the desired date-range
    :param datetime_end: a datetime object that indicates the exclusive upper bound of the desired date-range
    :return: An ordered list of datetime objects containing the days that are fully within the given range,
        as well as a tuple containing whether the left part and the right part of the date range have been consumed completely.
    """
    if datetime_begin > datetime_end:
        raise ValueError("date_begin cannot be larger than date_end")
    range_begin = datetime(datetime_begin.year, datetime_begin.month, datetime_begin.day)
    range_end = datetime(datetime_end.year, datetime_end.month, datetime_end.day)
    complete_l = True
    complete_r = True
    if datetime_begin.hour != 0 or datetime_begin.minute != 0:
        range_begin += timedelta(1)
        complete_l = False
    if datetime_end.hour != 0 or datetime_end.minute != 0:
        complete_r = False
    return [day for day in dtrange(range_begin, range_end, step=1, units='d')], (complete_l, complete_r)


def _chop_date_range_into_hours(datetime_begin, datetime_end):
    """
    Returns a range of hours (datetimes) that are fully within the given date range.
    :param datetime_begin: a datetime object that indicates the inclusive lower bound of the desired date-range
    :param datetime_end: a datetime object that indicates the exclusive upper bound of the desired date-range
    :return: An ordered list of datetime objects containing the hours that are fully within the given range,
        as well as a tuple containing whether the left part and the right part of the date range have been consumed completely.
    """
    if datetime_begin > datetime_end:
        raise ValueError("date_begin cannot be larger than date_end")
    range_begin = datetime(datetime_begin.year, datetime_begin.month, datetime_begin.day, datetime_begin.hour)
    range_end = datetime(datetime_end.year, datetime_end.month, datetime_end.day, datetime_end.hour)
    complete_l = True
    complete_r = True

    if datetime_begin.minute != 0:
        range_begin += timedelta(hours=1)
        complete_l = False
    if datetime_end.minute != 0:
        complete_r = False

    return [hour for hour in dtrange(range_begin, range_end, step=1, units='h')], (complete_l, complete_r)


def _chop_date_range_into_minutes(datetime_begin, datetime_end):
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
    # Reset both datetime_begin and datetime_end to the beginning of their minutes.
    datetime_begin -= timedelta(seconds=datetime_begin.second)
    datetime_end -= timedelta(seconds=datetime_end.second)

    num_minutes = int((datetime_end - datetime_begin).total_seconds() / 60)
    return [datetime_begin + minute * timedelta(seconds=60) for minute in range(num_minutes)]
