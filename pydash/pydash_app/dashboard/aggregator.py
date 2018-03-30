from collections import defaultdict
import datetime

import persistent


class Aggregator(persistent.Persistent):
    """
    Maintains aggregate data for either a dashboard or a single endpoint.
    This data is updated every time a new endpoint call is added.
    """

    def __init__(self, endpoint_calls=[]):
        """
        Constructor
        :param endpoint_calls: List of endpoint calls to keep track of
        """

        self._endpoint_calls = list(endpoint_calls)

        self.total_visits = 0
        self.total_execution_time = 0

        self.average_execution_time = None

        self.visits_per_day = defaultdict(int)
        self.visits_per_ip = defaultdict(int)

        self.unique_visitors_all_time_set = set()
        self.unique_visitors_per_day_set = defaultdict(set)

    def add_endpoint_call(self, endpoint_call):
        """
        Add an endpoint call and update aggregated data
        :param endpoint_call: `EndpointCall` instance to add
        """

        self._endpoint_calls.append(endpoint_call)

        self.total_visits += 1
        self.total_execution_time += endpoint_call.execution_time

        self.average_execution_time = self.total_execution_time / len(self._endpoint_calls)

        # day = endpoint_call.time.strftime('%Y-%m-%d')
        date = endpoint_call.time.date()
        self.visits_per_day[date] += 1

        self.visits_per_ip[endpoint_call.ip] += 1

        self.unique_visitors_all_time_set.add(endpoint_call.ip)
        self.unique_visitors_per_day_set[date].add(endpoint_call.ip)

    @property
    def unique_visitors_all_time(self):
        return len(self.unique_visitors_all_time_set)

    @property
    def unique_visitors_per_day(self):
        return {k: len(v) for k, v in self.unique_visitors_per_day_set.items()}

    def as_dict(self):
        """
        Get aggregated data in a dict
        :return: A dict containing several aggregated data points
        """

        def date_dict(dict):
            # JS expects dates in the ISO 8601 Date format (example: 2018-03)
            return {k.strftime("%Y-%m-%d"): v for (k, v) in dict.items()}

        return {
            'total_visits': self.total_visits,
            'total_execution_time': self.total_execution_time,
            'average_execution_time': self.average_execution_time,
            'visits_per_day': date_dict(self.visits_per_day),
            'visits_per_ip': dict(self.visits_per_ip),
            'unique_visitors': self.unique_visitors_all_time,
            'unique_visitors_per_day': date_dict(self.unique_visitors_per_day)
        }

