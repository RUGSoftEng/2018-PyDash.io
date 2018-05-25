from ordered_set import OrderedSet
from collections import OrderedDict

import persistent
from copy import deepcopy

from . import statistics


def date_dict(dict):
    # JS expects dates in the ISO 8601 Date format (example: 2018-03)
    return {k.strftime("%Y-%m-%d"): v for (k, v) in dict.items()}


class Aggregator(persistent.Persistent):
    """
    Maintains aggregate data for either a dashboard or a single endpoint.
    This data is updated every time a new endpoint call is added.
    """

    contained_statistics_classes = OrderedSet([
        statistics.TotalVisits,
        statistics.AverageExecutionTime,
        statistics.VisitsPerDay,
        statistics.VisitsPerIP,
        statistics.UniqueVisitorsAllTime,
        statistics.UniqueVisitorsPerDay,
        statistics.FastestExecutionTime,
        statistics.FastestQuartileExecutionTime,
        statistics.MedianExecutionTime,
        statistics.SlowestQuartileExecutionTime,
        statistics.NinetiethPercentileExecutionTime,
        statistics.NinetyNinthPercentileExecutionTime,
        statistics.SlowestExecutionTime,
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

    # Workaround for aggregator problem #323 for now
        from collections import defaultdict
        self._visits_per_day_dict = defaultdict(int)
        self._visits_per_day = defaultdict(int)
        self._visits_per_ip = defaultdict(int)
        self._unique_visitors = 0
        self._unique_visitors_set = set()
        self._unique_visitors_per_day = defaultdict(int)
        self._unique_visitors_per_day_set = defaultdict(set)

    # Workaround stops here

    def add_endpoint_call(self, endpoint_call):
        """
        Add an endpoint call and update aggregated data
        :param endpoint_call: `EndpointCall` instance to add
        """

        for statistic, value in self.statistics.items():
            value.append(endpoint_call, self.statistics)

        self.endpoint_calls.append(endpoint_call)

    #Workaround here again
        date = endpoint_call.time.date()
        self._visits_per_day_dict[date] += 1
        self._visits_per_day = date_dict(self._visits_per_day_dict)
        self._visits_per_ip[endpoint_call.ip] += 1
        self._unique_visitors_set.add(endpoint_call.ip)
        self._unique_visitors = len(self._unique_visitors_set)
        self._unique_visitors_per_day_set[date].add(endpoint_call.ip)
        self._unique_visitors_per_day = date_dict({k: len(v) for k, v in self._unique_visitors_per_day_set.items()})
    #Workaround stops here again

    def as_dict(self):
        """
        Return aggregated data in a dict. Only includes statistics that should be rendered.
        :return: A dict containing several aggregated data points
        """
        # return {
        #     statistic.field_name(): statistic.rendered_value()
        #     for statistic in self.statistics.values() if statistic.should_be_rendered
        # }

        initial_dict = {
            statistic.field_name(): statistic.rendered_value()
            for statistic in self.statistics.values() if statistic.should_be_rendered
        }
        initial_dict['visits_per_day'] = self._visits_per_day
        initial_dict['visits_per_ip'] = dict(self._visits_per_ip)
        initial_dict['unique_visitors'] = self._unique_visitors
        initial_dict['unique_visitors_per_day'] = self._unique_visitors_per_day

        return initial_dict

    def __add__(self, other):
        """Creates a new aggregator object that combines the aggregates of both aggegators."""
        if other is None:
            return deepcopy(self)

        new = Aggregator()
        new.endpoint_calls = self.endpoint_calls + other.endpoint_calls
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
        for key, _ in self.statistics.items():
            self.statistics[key] = self.satatistics[key].add_together(other.statistics[key], self.statistics, other.statistics)
        return self
