from ordered_set import OrderedSet
from collections import OrderedDict
from collections import defaultdict
import datetime

import persistent


def date_dict(dict):
    # JS expects dates in the ISO 8601 Date format (example: 2018-03)
    return {k.strftime("%Y-%m-%d"): v for (k, v) in dict.items()}


class Statistic(persistent.Persistent):
    dependencies = []
    def __init__(self):
        self.value = self.empty()

    def empty(self):
        return 0

    def append(self, endpoint_call):
        pass

    def field_name(self):
        pass

    def rendered_value(self):
        return self.value


class TotalVisitsStatistic(Statistic):
    def empty(self):
        return 0

    def field_name(self):
        return 'total_visits'

    def append(self, endpoint_call, dependencies):
        self.value += 1


class TotalExecutionTimeStatistic(Statistic):
    def empty(self):
        return 0

    def field_name(self):
        return 'total_execution_time'

    def append(self, endpoint_call, dependencies):
        self.value += endpoint_call.execution_time

class ExecutionTimeStatistic(Statistic):
    dependencies = [TotalVisitsStatistic, TotalExecutionTimeStatistic]
    def empty(self):
        return 0

    def field_name(self):
        return 'average_execution_time'

    def append(self, endpoint_call, dependencies):
        if dependencies[TotalVisitsStatistic].value == 0:
            self.value = 0
        else:
            self.value = dependencies[TotalExecutionTimeStatistic].value / dependencies[TotalVisitsStatistic].value

class VisitsPerDayStatistic(Statistic):
    dependencies = []
    def empty(self):
        return defaultdict(int)

    def field_name(self):
        return 'visits_per_day'

    def append(self, endpoint_call, dependencies):
        date = endpoint_call.time.date()
        self.value[date] += 1

    def rendered_value(self):
        return date_dict(self.value)


class VisitsPerIPStatistic(Statistic):
    dependencies = []
    def empty(self):
        return defaultdict(int)

    def field_name(self):
        return 'visits_per_ip'

    def append(self, endpoint_call, dependencies):
        self.value[endpoint_call.ip] += 1

    def rendered_value(self):
        return dict(self.value)

class UniqueVisitorsAllTimeStatistic(Statistic):
    dependencies = []
    def empty(self):
        return set()

    def field_name(self):
        return 'unique_visitors'

    def append(self, endpoint_call, dependencies):
        self.value.add(endpoint_call.ip)

    def rendered_value(self):
        return len(self.value)

class UniqueVisitorsPerDayStatistic(Statistic):
    dependencies = []
    def empty(self):
        return defaultdict(set)

    def field_name(self):
        return 'unique_visitors_per_day'

    def append(self, endpoint_call, dependencies):
        date = endpoint_call.time.date()
        self.value[date].add(endpoint_call.ip)

    def rendered_value(self):
        return {k: len(v) for k, v in self.value.items()}


class Aggregator2(persistent.Persistent):
    contained_statistics_classes = OrderedSet([
        TotalVisitsStatistic,
        ExecutionTimeStatistic,
        VisitsPerDayStatistic,
        VisitsPerIPStatistic,
        UniqueVisitorsPerDayStatistic,
        UniqueVisitorsAllTimeStatistic,
    ])
    statistics_classes_with_dependencies = OrderedSet()
    for statistic in contained_statistics_classes:
        for dependency in statistic.dependencies:
            statistics_classes_with_dependencies.add(dependency)
        statistics_classes_with_dependencies.add(statistic)

    def __init__(self, endpoint_calls=[]):
        self.endpoint_calls = []
        self.statistics = OrderedDict({statistic: statistic() for statistic in Aggregator2.statistics_classes_with_dependencies})
        for endpoint_call in endpoint_calls:
            self.add_endpoint_call(endpoint_call)

    def add_endpoint_call(self, endpoint_call):
        for statistic, value in self.statistics.items():
            value.append(endpoint_call, self.statistics)

        self.endpoint_calls.append(endpoint_call)

    def as_dict(self):
        return {statistic.field_name(): statistic.rendered_value() for statistic in self.statistics.values()}
