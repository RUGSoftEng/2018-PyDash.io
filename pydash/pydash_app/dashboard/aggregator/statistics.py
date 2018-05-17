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

    @property
    @abc.abstractmethod
    def should_be_rendered(self):
        """Note: implementing subclasses should add the @property decorator.
        There was some strange behaviour where without adding the decorator,
        subclasses implementing it as `return True` behaved normally, but those implementing it as `return False` still
        were treated as if it returned True. Adding the @property decorator fixed it.
        """
        pass

    @abc.abstractmethod
    def empty(self):
        return None

    @abc.abstractmethod
    def append(self, endpoint_call, dependencies):
        pass

    @abc.abstractmethod
    def field_name(self):
        pass

    def rendered_value(self):
        return self.value

    @classmethod
    def add_to_collection(cls, collection):
        """cls should only be a class instead of an instance."""
        for dependency in cls.dependencies:
            dependency.add_to_collection(collection)
        collection.add(cls)


class FloatStatisticABC(Statistic):
    """The FloatStatisticABC is the abstract base class for float rendering statistics.
    It specifies the default amount of decimal places to round its rendered value to as 3."""

    @property
    def rounded_decimal_places(self):
        return 3


class TotalVisits(Statistic):
    def should_be_rendered(self):
        return True

    def empty(self):
        return 0

    def field_name(self):
        return 'total_visits'

    def append(self, endpoint_call, dependencies):
        self.value += 1


class TotalExecutionTime(FloatStatisticABC):
    def should_be_rendered(self):
        return True

    def empty(self):
        return 0

    def field_name(self):
        return 'total_execution_time'

    def append(self, endpoint_call, dependencies):
        self.value += endpoint_call.execution_time

    def rendered_value(self):
        return round(self.value, self.rounded_decimal_places)


class AverageExecutionTime(FloatStatisticABC):
    """Keeps track of the average execution time of all endpoints that have been appended to it.
    Rendered value is rounded to 3 decimal places by default."""
    dependencies = [TotalVisits, TotalExecutionTime]

    def should_be_rendered(self):
        return True

    def empty(self):
        return 0

    def field_name(self):
        return 'average_execution_time'

    def append(self, endpoint_call, dependencies):
        if dependencies[TotalVisits].value == 0:
            self.value = 0
        else:
            self.value = dependencies[TotalExecutionTime].value / dependencies[TotalVisits].value

    def rendered_value(self):
        return round(self.value, self.rounded_decimal_places)


class VisitsPerDay(Statistic):
    def should_be_rendered(self):
        return True

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
    def should_be_rendered(self):
        return True

    def empty(self):
        return defaultdict(int)

    def field_name(self):
        return 'visits_per_ip'

    def append(self, endpoint_call, dependencies):
        self.value[endpoint_call.ip] += 1

    def rendered_value(self):
        return dict(self.value)


class UniqueVisitorsAllTime(Statistic):
    def should_be_rendered(self):
        return True

    def empty(self):
        return set()

    def field_name(self):
        return 'unique_visitors'

    def append(self, endpoint_call, dependencies):
        self.value.add(endpoint_call.ip)

    def rendered_value(self):
        return len(self.value)


class UniqueVisitorsPerDay(Statistic):
    def should_be_rendered(self):
        return True

    def empty(self):
        return defaultdict(set)

    def field_name(self):
        return 'unique_visitors_per_day'

    def append(self, endpoint_call, dependencies):
        date = endpoint_call.time.date()
        self.value[date].add(endpoint_call.ip)

    def rendered_value(self):
        return date_dict({k: len(v) for k, v in self.value.items()})


class ExecutionTimeTDigest(Statistic):
    """Acts as the general execution time tdigest, from which its dependants take their data from.
     This class is supposed to be instantiated, but not rendered."""
    def __init__(self):
        super().__init__()
        self.value = tdigest.TDigest()

    @property  # See Statistic.should_be_rendered
    def should_be_rendered(self):
        return False

    def empty(self):  # Implemented in order to be able to instantiate this class.
        return None

    def field_name(self):  # Implemented in order to be able to instantiate this class.
        return 'execution_time_tdigest'

    def append(self, endpoint_call, dependencies):
        self.value.update(endpoint_call.execution_time)


class ExecutionTimePercentileABC(FloatStatisticABC):
    """Abstract base class for execution time percentile statistics."""
    dependencies = [ExecutionTimeTDigest]
    _NoDataErrorValue = -1

    def __init__(self):
        super().__init__()
        self.value = self.empty()

    def should_be_rendered(self):
        return True

    def empty(self):
        return ExecutionTimePercentileABC._NoDataErrorValue

    def rendered_value(self):
        return round(self.value, self.rounded_decimal_places)


class FastestExecutionTime(ExecutionTimePercentileABC):
    def field_name(self):
        return 'fastest_measured_execution_time'

    def append(self, endpoint_call, dependencies):
        self.value = dependencies[ExecutionTimeTDigest].value.percentile(0)


class FastestQuartileExecutionTime(ExecutionTimePercentileABC):
    def field_name(self):
        return 'fastest_quartile_execution_time'

    def append(self, endpoint_call, dependencies):
        self.value = dependencies[ExecutionTimeTDigest].value.percentile(25)


class MedianExecutionTime(ExecutionTimePercentileABC):
    def field_name(self):
        return 'median_execution_time'

    def append(self, endpoint_call, dependencies):
        self.value = dependencies[ExecutionTimeTDigest].value.percentile(50)


class SlowestQuartileExecutionTime(ExecutionTimePercentileABC):
    def field_name(self):
        return 'slowest_quartile_execution_time'

    def append(self, endpoint_call, dependencies):
        self.value = dependencies[ExecutionTimeTDigest].value.percentile(75)


class NinetiethPercentileExecutionTime(ExecutionTimePercentileABC):
    def field_name(self):
        return 'ninetieth_percentile_execution_time'

    def append(self, endpoint_call, dependencies):
        self.value = dependencies[ExecutionTimeTDigest].value.percentile(90)


class NinetyNinthPercentileExecutionTime(ExecutionTimePercentileABC):
    def field_name(self):
        return 'ninety-ninth_percentile_execution_time'

    def append(self, endpoint_call, dependencies):
        self.value = dependencies[ExecutionTimeTDigest].value.percentile(99)


class SlowestExecutionTime(ExecutionTimePercentileABC):
    def field_name(self):
        return 'slowest_measured_execution_time'

    def append(self, endpoint_call, dependencies):
        self.value = dependencies[ExecutionTimeTDigest].value.percentile(100)
