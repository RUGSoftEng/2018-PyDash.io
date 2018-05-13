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
        statistics.FastestExecutionTime,
        statistics.FastestQuartileExecutionTime,
        statistics.SlowestQuartileExecutionTime,
        statistics.NinetiethPercentileExecutionTime,
        statistics.NinetyNinthPercentileExecutionTime,
        statistics.SlowestExecutionTime,
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
