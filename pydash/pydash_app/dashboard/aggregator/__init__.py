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
        statistics.AverageExecutionTime,
        # statistics.VisitsPerDay,
        statistics.VisitsPerIP,
        statistics.UniqueVisitorsAllTime,
        # statistics.UniqueVisitorsPerDay,
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
        """Creates a new aggregator object that combines the aggregates of both aggegators."""
        if other is None:
            return deepcopy(self)

        new = Aggregator()
        new.endpoint_calls += self.endpoint_calls
        new.endpoint_calls += other.endpoint_calls
        for key, _ in new.statistics.items():
            new.statistics[key] = self.statistics[key].add_together(other.statistics[key], self.statistics, other.statistics)
        return new

    def __radd__(self, other):
        # Return a deep copy in case sum(<Aggregator iterable>) is called
        if other == 0:
            return self.deepcopy()
        else:
            return self.__add__(other)

    def __iadd__(self, other):

        if other is None:
            return self
        self.endpoint_calls += other.endpoint_calls
        for key in self.statistics.keys():
            self.statistics[key] = self.statistics[key].add_together(other.statistics[key], self.statistics, other.statistics)
        return self
