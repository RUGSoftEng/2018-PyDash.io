import persistent
import datetime
from collections import namedtuple, defaultdict


class UptimeLog(persistent.Persistent):
    """
    Keeps track of uptime, and calculates downtime intervals, total downtime, and downtime percentage
    in an on-line manner.
    """

    def __init__(self):
        self._downtime_intervals = defaultdict(list)  # datetime.date -> list[(datetime.time, datetime.time)]
        self._total_downtime = defaultdict(datetime.timedelta)  # datetime.date -> datetime.timedelta

        self._downtime_start = None

    def add_ping_result(self, is_up, ping_datetime=datetime.datetime.now(tz=datetime.timezone.utc)):
        """
        Add the result of a ping request to the uptime log.
        :param is_up: Whether the web service is up or not.
        :param ping_datetime: When the ping took place (approximately); defaults to the current time in UTC.
        """


