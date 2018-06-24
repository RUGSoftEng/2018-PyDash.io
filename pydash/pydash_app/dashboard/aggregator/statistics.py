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
    """
    Converts a {datetime: value} dictionary to a {datetime_formatted_string: value} dictionary,
    where the string is formatted according to the ISO 6801 Date format (representing a day).

    Example:
    >>> from datetime import datetime
    >>> dictionary = {datetime(1970,1,1): "Foo"}
    >>> date_dict(dictionary)
    {'1970-01-01': 'Foo'}
    """
    # JS expects dates in the ISO 8601 Date format (example: 2018-03)
    return {k.strftime("%Y-%m-%d"): v for (k, v) in dict.items()}


class Statistic(persistent.Persistent, abc.ABC):
    """Aggregates a single statistic value."""
    dependencies = []

    def __init__(self):
        self.value = self.empty()

    @property
    @abc.abstractmethod
    def should_be_rendered(self):
        """
        Indicates whether this Statistic instance should be rendered or not. The latter would be the case for statistics
        that solely serve as dependencies for other statistics.

        Note: implementing subclasses should add the @property decorator.
        There was some strange behaviour where without adding the decorator,
        subclasses implementing it as `return True` behaved normally, but those implementing it as `return False` still
        were treated as if it returned True. Adding the @property decorator fixed it.
        """
        pass

    @abc.abstractmethod
    def empty(self):
        """Returns the empty state of self.value, such that it contains no data of any endpoint calls."""
        return None

    def append(self, endpoint_call, dependencies):
        """Wrapper for perform_append, that makes sure this Statistic instance is marked as changed for a ZODB database."""
        self.perform_append(endpoint_call, dependencies)
        self._p_changed = True  # ZODB mark object as changed

    @abc.abstractmethod
    def perform_append(self, endpoint_call, dependencies):
        """Updates self.value to reflect the addition/appending of the given endpoint call, given its dependencies."""
        pass

    @classmethod
    @abc.abstractmethod
    def field_name(cls):
        pass

    def rendered_value(self):
        return self.value

    @classmethod
    def add_to_collection(cls, collection):
        """
        Adds this Statistic instance and its dependencies to a collection.
        cls should only be a class instead of an instance.
        """
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
        """Number of digits to round its rendered value to. See reduce_precision()."""
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
    """Total execution time in ms. Rendered value is rounded to 3 decimal places by default."""
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
    """Keeps track of the average execution time in ms of all endpoints that have been appended to it.
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


class Versions(Statistic):
    def should_be_rendered(self):
        return True

    def empty(self):
        return set()

    def field_name(self):
        return 'versions'

    def rendered_value(self):
        return list(self.value)

    def perform_append(self, endpoint_call, dependencies):
        self.value.add(endpoint_call.version)

    def add_together(self, other, dependencies_self, dependencies_other):
        versions = Versions()
        versions.value = self.value.union(other.value)
        return versions
