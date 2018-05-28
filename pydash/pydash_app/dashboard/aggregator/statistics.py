from collections import defaultdict
import abc
from tdigest import tdigest
from math import trunc

import persistent


def reduce_precision(value, nr_of_digits):
    """
    Reduces the precision of `value` based on the amount of non-zero digits before the decimal point
    and `nr_of_digits`.

    Examples:
    >>> x = 2/3
    >>> reduce_precision(x, 3)
    0.67
    >>> x = 1234.5678
    >>> reduce_precision(x, 3)
    1235

    """
    x = len(str(trunc(value)))
    y = (nr_of_digits-x)
    if y <= 0:
        return trunc(round(value, 0))
    else:
        return round(value, y)


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

    def append(self, endpoint_call, dependencies):
        self.perform_append(endpoint_call, dependencies)
        self._p_changed = True # ZODB mark object as changed

    @abc.abstractmethod
    def perform_append(self, endpoint_call, dependencies):
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

    @abc.abstractmethod
    def add_together(self, other, dependencies_self, dependencies_other):
        """Should return a new statistic where the internals of self and other are added together."""
        pass


class FloatStatisticABC(Statistic):
    """
    The FloatStatisticABC is the abstract base class for statistics that render a single floating point number.
    It specifies the default amount of digits to round its rendered value to as 3.
    (E.g. 2.54, 123, 0.3, but not 0.123)
    """

    @property
    def nr_of_digits(self):
        return 3

    def rendered_value(self):
        return reduce_precision(self.value, self.nr_of_digits)


class TotalVisits(Statistic):
    def should_be_rendered(self):
        return True

    def empty(self):
        return 0

    def field_name(self):
        return 'total_visits'

    def perform_append(self, endpoint_call, dependencies):
        self.value += 1

    def add_together(self, other, dependencies_self, dependencies_other):
        tv = TotalVisits()
        tv.value = self.value + other.value
        return tv


class TotalExecutionTime(FloatStatisticABC):
    def should_be_rendered(self):
        return True

    def empty(self):
        return 0

    def field_name(self):
        return 'total_execution_time'

    def perform_append(self, endpoint_call, dependencies):
        self.value += endpoint_call.execution_time

    def add_together(self, other, dependencies_self, dependencies_other):
        te = TotalExecutionTime()
        te.value = self.value + other.value
        return te


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

    def perform_append(self, endpoint_call, dependencies):
        if dependencies[TotalVisits].value == 0:
            self.value = 0
        else:
            self.value = dependencies[TotalExecutionTime].value / dependencies[TotalVisits].value

    def add_together(self, other, dependencies_self, dependencies_other):
        aet = AverageExecutionTime()
        self_tv = dependencies_self[TotalVisits].value
        other_tv = dependencies_other[TotalVisits].value
        self_tet = dependencies_self[TotalExecutionTime].value
        other_tet = dependencies_other[TotalExecutionTime].value

        if self_tv == 0:
            aet.value = other.value
        elif other_tv == 0:
            aet.value = self.value
        else:
            aet.value = (self_tet + other_tet)/(self_tv + other_tv)

        return aet


class VisitsPerDay(Statistic):
    def should_be_rendered(self):
        return True

    def empty(self):
        return defaultdict(int)

    def field_name(self):
        return 'visits_per_day'

    def perform_append(self, endpoint_call, dependencies):
        date = endpoint_call.time.date()
        self.value[date] += 1

    def rendered_value(self):
        return date_dict(self.value)

    def add_together(self, other, dependencies_self, dependencies_other):
        vpd = VisitsPerDay()
        keyset = set(self.value.keys()).union(set(other.value.keys()))
        for key in keyset:
            vpd.value[key] = self.value[key] + other.value[key]
        return vpd


class VisitsPerIP(Statistic):
    def should_be_rendered(self):
        return True

    def empty(self):
        return defaultdict(int)

    def field_name(self):
        return 'visits_per_ip'

    def perform_append(self, endpoint_call, dependencies):
        self.value[endpoint_call.ip] += 1

    def rendered_value(self):
        return dict(self.value)

    def add_together(self, other, dependencies_self, dependencies_other):
        vpd = VisitsPerIP()
        keyset = set(self.value.keys()).union(set(other.value.keys()))
        for key in keyset:
            vpd.value[key] = self.value[key] + other.value[key]
        return vpd


class UniqueVisitorsAllTime(Statistic):
    def should_be_rendered(self):
        return True

    def empty(self):
        return set()

    def field_name(self):
        return 'unique_visitors'

    def perform_append(self, endpoint_call, dependencies):
        self.value.add(endpoint_call.ip)

    def rendered_value(self):
        return len(self.value)

    def add_together(self, other, dependencies_self, dependencies_other):
        uvat = UniqueVisitorsAllTime()
        uvat.value = self.value.union(other.value)
        return uvat


class UniqueVisitorsPerDay(Statistic):
    def should_be_rendered(self):
        return True

    def empty(self):
        return defaultdict(set)

    def field_name(self):
        return 'unique_visitors_per_day'

    def perform_append(self, endpoint_call, dependencies):
        date = endpoint_call.time.date()
        self.value[date].add(endpoint_call.ip)

    def rendered_value(self):
        return date_dict({k: len(v) for k, v in self.value.items()})

    def add_together(self, other, dependencies_self, dependencies_other):
        uvpd = UniqueVisitorsPerDay()
        keyset = set(self.value.keys()).union(set(other.value.keys()))
        for key in keyset:
            uvpd.value[key] = self.value[key].union(other.value[key])
        return uvpd


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

    def perform_append(self, endpoint_call, dependencies):
        self.value.update(endpoint_call.execution_time)

    def add_together(self, other, dependencies_self, dependencies_other):
        ettd = ExecutionTimeTDigest()
        ettd.value = self.value + other.value
        return ettd


class ExecutionTimePercentileABC(FloatStatisticABC):
    """Abstract base class for execution time percentile statistics."""
    dependencies = [ExecutionTimeTDigest]
    _NoDataErrorValue = -1

    def __init__(self):
        super().__init__()
        self.value = self.empty()

    @property
    @abc.abstractmethod
    def percentile_nr(self):
        pass

    def should_be_rendered(self):
        return True

    def empty(self):
        return ExecutionTimePercentileABC._NoDataErrorValue

    def perform_append(self, endpoint_call, dependencies):
        # self.percentile_nr is called here, as in child classes it is interpreted as a method instead of a value
        #  for some reason.
        self.value = dependencies[ExecutionTimeTDigest].value.percentile(self.percentile_nr())

    def add_together(self, other, dependencies_self, dependencies_other):
        etp = self.__class__()

        if other.value == other.empty():
            etp.value = self.value
        else:
            # self.percentile_nr is called here, as in child classes it is interpreted as a method instead of a value
            #  for some reason.
            etp.value = (dependencies_self[ExecutionTimeTDigest].value +
                         dependencies_other[ExecutionTimeTDigest].value) \
                .percentile(self.percentile_nr())
        return etp


class FastestExecutionTime(ExecutionTimePercentileABC):
    def field_name(self):
        return 'fastest_measured_execution_time'

    def percentile_nr(self):
        return 0


class FastestQuartileExecutionTime(ExecutionTimePercentileABC):
    def field_name(self):
        return 'fastest_quartile_execution_time'

    def percentile_nr(self):
        return 25


class MedianExecutionTime(ExecutionTimePercentileABC):
    def field_name(self):
        return 'median_execution_time'

    def percentile_nr(self):
        return 50


class SlowestQuartileExecutionTime(ExecutionTimePercentileABC):
    def field_name(self):
        return 'slowest_quartile_execution_time'

    def percentile_nr(self):
        return 75


class NinetiethPercentileExecutionTime(ExecutionTimePercentileABC):
    def field_name(self):
        return 'ninetieth_percentile_execution_time'

    def percentile_nr(self):
        return 90


class NinetyNinthPercentileExecutionTime(ExecutionTimePercentileABC):
    def field_name(self):
        return 'ninety-ninth_percentile_execution_time'

    def percentile_nr(self):
        return 99


class SlowestExecutionTime(ExecutionTimePercentileABC):
    def field_name(self):
        return 'slowest_measured_execution_time'

    def percentile_nr(self):
        return 100
