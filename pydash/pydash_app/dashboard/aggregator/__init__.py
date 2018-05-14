from ordered_set import OrderedSet
from collections import OrderedDict

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
        yield set(subset)

class AggregatorPartitionFun(abc.ABC):

    @abc.abstractmethod
    def __call__(self, endpoint_call):
        pass

    @abc.abstractmethod
    def field_name(self):
        pass

    def __eq__(self):
        """
        AggregatorPartitionFuns with the same category
        will not be part of the same selector in the AggregatorGroup.
        This ensures we can e.g. have multiple different ways to partition in time,
        that are mutually exclusive.
        """
        return super(self)

class PartitionByWeek(AggregatorPartitionFun):
    def __call__(self, endpoint_call):
        return endpoint_call.time.strftime("%Y-W%W")

    def __eq__(self):
        return 'time'

class PartitionByDay(AggregatorPartitionFun):
    def __call__(self, endpoint_call):
        return endpoint_call.time.strftime("%Y-%m-%d")

    def __eq__(self):
        return 'time'

class PartitionByHour(AggregatorPartitionFun):
    def __call__(self, endpoint_call):
        return endpoint_call.time.strftime("%Y-%m-%dT%H")

    def __eq__(self):
        return 'time'

class PartitionByIP(AggregatorPartitionFun):
    def __call__(self, endpoint_call):
        return endpoint_call.ip

class PartitionByGroupBy(AggregatorPartitionFun):
    def __call__(self, endpoint_call):
        return endpoint_call.group_by

class AggregatorGroup(persistent.Persistent):
    """
    Maintains a powerset of dicts of aggregators,
    such that we can filter based on:
    - time
    - IP
    - FMD's group_by
    - etc.
    """
    partition_funs = set([
        PartitionByGroupBy,
        PartitionByIP,
        PartitionByWeek,
        PartitionByDay,
        PartitionByHour,
    ])

    partition_powerset = powerset(partition_funs)

    def __init__(self):
        self.partitions = dict()
        for elem in partition_powerset:
            self.partitions[elem] = defaultdict(Aggregator)

    def add_endpoint_call(self, endpoint_call):
        for (partition, vals) in self.partitions.items():
            endpoint_call_identifier = calc_endpoint_call_identifier(partition, endpoint_call)
            vals[endpoint_call_identifier].add_endpoint_call(endpoint_call)
    def calc_endpoint_identifier(self, partition, endpoint_call):
        return tuple(partition_fun(endpoint_call) for partition_fun in partition)
