"""
Exposes the class DowntimeLog, which keeps track of a web service's downtime,
and calculates downtime intervals, total downtime, and downtime percentage
in an on-line manner.
"""

import persistent
import datetime
from collections import defaultdict


class DowntimeLog(persistent.Persistent):
    """
    Keeps track of downtime, and calculates downtime intervals, total downtime, and downtime percentage
    in an on-line manner.
    """

    def __init__(self):
        self._downtime_intervals = defaultdict(list)  # datetime.date -> list[(datetime.time, datetime.time)]
        self._total_downtime = defaultdict(datetime.timedelta)  # datetime.date -> datetime.timedelta

        self._downtime_start = None

    def add_ping_result(self, is_up, ping_datetime=datetime.datetime.now(tz=datetime.timezone.utc)):
        """
        Add the result of a ping request to the downtime log.
        :param is_up: Whether the web service is up or not.
        :param ping_datetime: When the ping took place (approximately); defaults to the current time in UTC.
        """
        if is_up:
            if self._downtime_start:
                # Split the downtime into intervals of at most 24 hours

                start = self._downtime_start
                end = min(ping_datetime, _day_end(start))

                while start <= ping_datetime:
                    date = start.date()
                    interval = (start.timetz(), end.timetz())
                    self._downtime_intervals[date].append(interval)
                    self._total_downtime[date] += (end - start) + datetime.timedelta(microseconds=1)

                    start = _day_start(start + datetime.timedelta(days=1))
                    end = min(ping_datetime, _day_end(start))

                self._downtime_start = None
        else:
            if self._downtime_start is None:
                self._downtime_start = ping_datetime

    def get_downtime_intervals(
            self,
            start=datetime.datetime.now(tz=datetime.timezone.utc).date() - datetime.timedelta(days=90),
            end=datetime.datetime.now(tz=datetime.timezone.utc).date()):
        """
        Return the intervals of downtime per day between two dates.
        :param start: The start date (exclusive; defaults to 90 days before the current day).
        :param end: The end date (inclusive; defaults to the current day).
        :return: A dict containing a list of downtime intervals per day.
        """
        if end <= start:
            ValueError('Date range cannot be negative or zero')

        return {
            date.strftime('%Y-%m-%d'): list(self._downtime_intervals[date])
            for date in _date_range(start, end)
        }

    def get_total_downtimes(
            self,
            start=datetime.datetime.now(tz=datetime.timezone.utc).date() - datetime.timedelta(days=90),
            end=datetime.datetime.now(tz=datetime.timezone.utc).date()):
        """
        Return the total amounts of downtime per day between two dates.
        :param start: The start date (exclusive; defaults to 90 days before the current day).
        :param end: The end date (inclusive; defaults to the current day).
        :return: A dict containing the total downtime per day.
        """
        if end <= start:
            raise ValueError('Date range cannot be negative or zero')

        return {
            date.strftime('%Y-%m-%d'): self._total_downtime[date]
            for date in _date_range(start, end)
        }

    def get_downtime_percentage(
            self,
            start=datetime.datetime.now(tz=datetime.timezone.utc).date() - datetime.timedelta(days=90),
            end=datetime.datetime.now(tz=datetime.timezone.utc).date()):
        """
        Get the percentage of downtime between two dates.
        :param start: The start date (exclusive; defaults to 90 days before the current day).
        :param end: The end date (inclusive; defaults to the current day).
        :return: A float, the downtime percentage for the given date range.
        """
        if end <= start:
            raise ValueError('Date range cannot be negative or zero')

        total_downtime = sum(
            (self._total_downtime[date] for date in _date_range(start, end)),
            datetime.timedelta(0)
        )

        total_time = end - start

        percentage = total_downtime/total_time*100

        return percentage


def _day_start(dt):
    return datetime.datetime.combine(dt.date(), datetime.time.min).replace(tzinfo=datetime.timezone.utc)


def _day_end(dt):
    return datetime.datetime.combine(dt.date(), datetime.time.max).replace(tzinfo=datetime.timezone.utc)


def _date_range(start, end):
    """
    Yield dates in the range (start, end].
    :param start: Start date (exclusive).
    :param end: End date.
    """
    start += datetime.timedelta(days=1)
    while start <= end:
        yield start
        start += datetime.timedelta(days=1)
