from collections import defaultdict
import abc
from tdigest import tdigest

import persistent


def date_dict(dict):
    # JS expects dates in the ISO 8601 Date format (example: 2018-03)
    return {k.strftime("%Y-%m-%d"): v for (k, v) in dict.items()}


class Statistic(persistent.Persistent, abc.ABC):
    dependencies = []

    def __init__(self):
        self.value = self.empty()

    @abc.abstractmethod
    def empty(self):
        return None

    @abc.abstractmethod
    def append(self, endpoint_call):
        pass

    @abc.abstractmethod
    def field_name(self):
        pass

    def rendered_value(self):
        return self.value


class TotalVisits(Statistic):
    def empty(self):
        return 0

    def field_name(self):
        return 'total_visits'

    def append(self, endpoint_call, dependencies):
        self.value += 1


class TotalExecutionTime(Statistic):
    def empty(self):
        return 0

    def field_name(self):
        return 'total_execution_time'

    def append(self, endpoint_call, dependencies):
        self.value += endpoint_call.execution_time


class ExecutionTime(Statistic):
    dependencies = [TotalVisits, TotalExecutionTime]

    def empty(self):
        return 0

    def field_name(self):
        return 'average_execution_time'

    def append(self, endpoint_call, dependencies):
        if dependencies[TotalVisits].value == 0:
            self.value = 0
        else:
            self.value = dependencies[TotalExecutionTime].value / dependencies[TotalVisits].value


class VisitsPerDay(Statistic):
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


class VisitsPerIP(Statistic):
    dependencies = []

    def empty(self):
        return defaultdict(int)

    def field_name(self):
        return 'visits_per_ip'

    def append(self, endpoint_call, dependencies):
        self.value[endpoint_call.ip] += 1

    def rendered_value(self):
        return dict(self.value)


class UniqueVisitorsAllTime(Statistic):
    dependencies = []

    def empty(self):
        return set()

    def field_name(self):
        return 'unique_visitors'

    def append(self, endpoint_call, dependencies):
        self.value.add(endpoint_call.ip)

    def rendered_value(self):
        return len(self.value)


class UniqueVisitorsPerDay(Statistic):
    dependencies = []

    def empty(self):
        return defaultdict(set)

    def field_name(self):
        return 'unique_visitors_per_day'

    def append(self, endpoint_call, dependencies):
        date = endpoint_call.time.date()
        self.value[date].add(endpoint_call.ip)

    def rendered_value(self):
        return date_dict({k: len(v) for k, v in self.value.items()})


class FastestExecutionTime(Statistic):
    dependencies = []

    def empty(self):
        return -1

    def field_name(self):
        return 'fastest_measured_execution_time'

    def append(self, endpoint_call, dependencies):
        if self.value < 0 or self.value > endpoint_call.execution_time:
            self.value = endpoint_call.execution_time

    def rendered_value(self):
        return self.value


class SlowestExecutionTime(Statistic):
    dependencies = []

    def empty(self):
        return -1

    def field_name(self):
        return 'slowest_measured_execution_time'

    def append(self, endpoint_call, dependencies):
        if self.value < endpoint_call.execution_time:
            self.value = endpoint_call.execution_time

    def rendered_value(self):
        return self.value


class TDigestStatistic(Statistic):
    dependencies = []

    def __init__(self):
        super().__init__()
        self.value = self.empty()
        self._digest = tdigest.TDigest()

    def empty(self):
        return -1

    @abc.abstractmethod
    def field_name(self):
        pass

    @abc.abstractmethod
    def append(self, endpoint_call, dependencies):
        self._digest.update(endpoint_call.execution_time)

    def rendered_value(self):
        return self.value


class FastestQuartileExecutionTime(TDigestStatistic):
    dependencies = []

    def field_name(self):
        return 'fastest_quartile_execution_time'

    def append(self, endpoint_call, dependencies):
        super().append(endpoint_call, dependencies)
        self.value = self._digest.percentile(25)


class SlowestQuartileExecutionTime(TDigestStatistic):
    dependencies = []

    def field_name(self):
        return 'slowest_quartile_execution_time'

    def append(self, endpoint_call, dependencies):
        super().append(endpoint_call, dependencies)
        self.value = self._digest.percentile(75)


class NinetiethPercentileExecutionTime(TDigestStatistic):
    dependencies = []

    def field_name(self):
        return 'ninetieth_percentile_execution_time'

    def append(self, endpoint_call, dependencies):
        super().append(endpoint_call, dependencies)
        self.value = self._digest.percentile(90)


class NinetyNinthPercentileExecutionTime(TDigestStatistic):
    dependencies = []

    def field_name(self):
        return 'ninety-ninth_percentile_execution_time'

    def append(self, endpoint_call, dependencies):
        super().append(endpoint_call, dependencies)
        self.value = self._digest.percentile(99)
