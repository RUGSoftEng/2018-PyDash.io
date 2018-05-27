import persistent
import datetime
from collections import defaultdict


class UptimeLog(persistent.Persistent):
    """
    Keeps track of uptime, and calculates downtime intervals, total downtime, and downtime percentage
    in an on-line manner.
    """

    def __init__(self):
        self._log = defaultdict(list)  # datetime.date -> list[(datetime.time, bool)]
        self._downtime = defaultdict(list)  # datetime.date -> list[(datetime.time, datetime.time)]
        self._total_downtime = defaultdict(datetime.timedelta)  # datetime.date -> datetime.timedelta
        self._up_percentage = defaultdict(float)  # datetime.date -> float

        self._is_up = None

    def add_ping_result(self, is_up, ping_time=datetime.datetime.now(tz=datetime.timezone.utc)):
        ping_date = ping_time.date()
        status = (ping_time.time(), is_up)
        self._log[ping_date].append(status)
