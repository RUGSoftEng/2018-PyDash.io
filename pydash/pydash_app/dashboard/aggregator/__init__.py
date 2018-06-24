from ordered_set import OrderedSet
from collections import OrderedDict

import persistent
from copy import deepcopy

from . import statistics


class Aggregator(persistent.Persistent):
    """
    Maintains aggregate data for either a dashboard or a single endpoint.
    This data is updated every time a new endpoint call is added.
    """

    contained_statistics_classes = OrderedSet([
        statistics.TotalVisits,
        statistics.TotalExecutionTime,
        statistics.AverageExecutionTime,
        statistics.VisitsPerIP,
        statistics.UniqueVisitorsAllTime,
        statistics.FastestExecutionTime,
        statistics.FastestQuartileExecutionTime,
        statistics.MedianExecutionTime,
        statistics.SlowestQuartileExecutionTime,
        statistics.NinetiethPercentileExecutionTime,
        statistics.NinetyNinthPercentileExecutionTime,
        statistics.SlowestExecutionTime,
        statistics.Versions,
    ])
    statistics_classes_with_dependencies = OrderedSet()
    for statistic in contained_statistics_classes:
        statistic.add_to_collection(statistics_classes_with_dependencies)

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
        self._p_changed = True  # ZODB mark object as changed

    def as_dict(self):
        """
        Return aggregated data in a dict. Only includes statistics that should be rendered.
        :return: A dict containing several aggregated data points
        """

        return {
            statistic.field_name(): statistic.rendered_value()
            for statistic in self.statistics.values() if statistic.should_be_rendered
        }

    def __add__(self, other):
        """Creates a new Aggregator instance that combines the aggregates of both aggegators."""
        if other is None:
            return deepcopy(self)

        new = Aggregator()
        new.endpoint_calls = [endpoint_call for endpoint_call in set(self.endpoint_calls).union(set(other.endpoint_calls))]
        for key, _ in new.statistics.items():
            new.statistics[key] = self.statistics[key].add_together(other.statistics[key], self.statistics, other.statistics)
        return new

    def __radd__(self, other):
        """Creates a new Aggregator instance that combines the aggregates of both aggregators.
         If other == 0 (e.g. when using sum() on an iterable of Aggregators), returns a copy of itself."""
        # Return a deep copy in case sum(<Aggregator iterable>) is called
        if other == 0:
            return self.deepcopy()
        else:
            return self.__add__(other)

    def __iadd__(self, other):
        """In-place version of _add_()."""
        if other is None:
            return self
        self.endpoint_calls = [endpoint_call for endpoint_call in set(self.endpoint_calls).union(set(other.endpoint_calls))]
        for key in self.statistics.keys():
            self.statistics[key] = self.statistics[key].add_together(other.statistics[key], self.statistics, other.statistics)
        return self
