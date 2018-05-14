import abc
import itertools

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
