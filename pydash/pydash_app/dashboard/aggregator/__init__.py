from ordered_set import OrderedSet
from collections import OrderedDict

import abc
from collections import defaultdict
from itertools import chain, combinations

import persistent

from . import statistics


class Aggregator(persistent.Persistent):
    """
    Maintains aggregate data for either a dashboard or a single endpoint.
    This data is updated every time a new endpoint call is added.
    """

    contained_statistics_classes = OrderedSet([
        statistics.TotalVisits,
        statistics.ExecutionTime,
        statistics.VisitsPerDay,
        statistics.VisitsPerIP,
        statistics.UniqueVisitorsAllTime,
        statistics.UniqueVisitorsPerDay,
    ])
    statistics_classes_with_dependencies = OrderedSet()
    for statistic in contained_statistics_classes:
        for dependency in statistic.dependencies:
            statistics_classes_with_dependencies.add(dependency)
        statistics_classes_with_dependencies.add(statistic)

    def __init__(self, endpoint_calls=[]):
        """
        Constructor
        :param endpoint_calls: List of endpoint calls to keep track of
        """
        self.endpoint_calls = []
        self.statistics = OrderedDict({
            statistic: statistic()
            for statistic in Aggregator.statistics_classes_with_dependencies
        })
        for endpoint_call in endpoint_calls:
            self.add_endpoint_call(endpoint_call)

    def add_endpoint_call(self, endpoint_call):
        """
        Add an endpoint call and update aggregated data
        :param endpoint_call: `EndpointCall` instance to add
        """

        for statistic, value in self.statistics.items():
            value.append(endpoint_call, self.statistics)

        self.endpoint_calls.append(endpoint_call)

    def as_dict(self):
        """
        Return aggregated data in a dict
        :return: A dict containing several aggregated data points
        """

        return {
            statistic.field_name(): statistic.rendered_value()
            for statistic in self.statistics.values()
        }


def powerset_generator(i):
    for subset in chain.from_iterable(combinations(i, r) for r in range(len(i)+1)):
        yield list(subset)


class AggregatorPartitionFun():
    def __init__(self, field_name, category, fun):
        self.field_name = field_name
        self.fun = fun
        self.category = category

    def __call__(self, endpoint_call):
        self.fun(endpoint_call)

    def __repr__(self):
        return f"<{self.__class__.__name__} field_name={self.field_name} category={self.category} >"

def partition_by_year_fun(endpoint_call):
    return endpoint_call.time.strftime("%Y")
PartitionByYear = AggregatorPartitionFun('year', 'time', partition_by_year_fun)

def partition_by_week_fun(endpoint_call):
    return endpoint_call.time.strftime("%Y-W%W")
PartitionByWeek = AggregatorPartitionFun('week', 'time', partition_by_week_fun)


def partition_by_day_fun(endpoint_call):
    return endpoint_call.time.strftime("%Y-%M-%d")
PartitionByDay = AggregatorPartitionFun('day', 'time', partition_by_day_fun)

def partition_by_hour_fun(endpoint_call):
    return endpoint_call.time.strftime("%Y-%m-%dT%H")
PartitionByHour = AggregatorPartitionFun('hour', 'time', partition_by_hour_fun)

def partition_by_ip_fun(endpoint_call):
    def __call__(self, endpoint_call):
        return endpoint_call.ip
PartitionByIP = AggregatorPartitionFun('ip', 'ip', partition_by_ip_fun)

def partition_by_group_by_fun(endpoint_call):
    def __call__(self, endpoint_call):
        return endpoint_call.group_by
PartitionByGroupBy = AggregatorPartitionFun('group_by', 'group_by', partition_by_group_by_fun)


def remove_duplicate_categories(partition_funs):
    categories = set()
    print(partition_funs)
    for partition_fun in partition_funs:
        if(partition_fun.category in categories):
            next
        else:
            categories.add(partition_fun.category)
            yield partition_fun


def calc_endpoint_call_identifier(partition, endpoint_call):
    return tuple(partition_fun(endpoint_call) for partition_fun in partition)

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
    """
    partition_funs = [
        PartitionByWeek,
        PartitionByDay,
        PartitionByHour,
        PartitionByGroupBy,
        PartitionByIP,
    ]

    partition_powerset = powerset_generator(partition_funs)
    partitions_set = frozenset(frozenset(remove_duplicate_categories(elem)) for elem in partition_powerset)
    for partition in partitions_set:
        print(partition)

    def __init__(self):
        self.partitions = dict()
        self.partition_names = dict()
        for elem in self.partitions_set:
            self.partitions[elem] = defaultdict(Aggregator)
            self.partition_names[frozenset(partition_field_names(elem))] = elem

    def add_endpoint_call(self, endpoint_call):
        for (partition, vals) in self.partitions.items():
            endpoint_call_identifier = calc_endpoint_call_identifier(partition, endpoint_call)
            vals[endpoint_call_identifier].add_endpoint_call(endpoint_call)

    def fetch(self, **partition_field_names):
        partition = self.partition_names[frozenset(partition_field_names.keys())]
        return self.partitions[partition][partition_field_names.values]


# import pydash_app
# ec = pydash_app.dashboard.repository.all()[1]._endpoint_calls[0]
# a = pydash_app.dashboard.aggregator.AggregatorGroup()
# a.add_endpoint_call(ec)
