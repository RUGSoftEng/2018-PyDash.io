
import persistent
from flask import jsonify


class EndpointCall(persistent.Persistent):
    """
    An EndpointCall entity only serves to store JSON data pulled from the external dashboards.

    As with the other entity classes, it does not concern itself with the implementation of its persistence,
    as it doesn't exist on its own.
    If this were the case, the `endpointcall_repository` would handle this concern.
    """

    def __init__(self, endpoint, execution_time, time, version, group_by, ip):
        """
        Wrapper that embodies the resulting json fields of an endpoint call.
        :param endpoint: String denoting the endpoint's name.
        :param execution_time: Float denoting the execution time of the endpoint call.
        :param time: Timestamp denoting the time the endpoint call was made.
        :param version: Float (?) denoting the dashboard's version number.
        :param group_by: String denoting which user is calling the function (?).
        :param ip: String denoting the IP-address the endpoint call was made from.
        """

        self.data = jsonify(endpoint=endpoint, execution_time=execution_time, time=time, version=version,
                            group_by=group_by, ip=ip)
        # self.endpoint = endpoint  # string
        # self.execution_time = execution_time  # float
        # self.time = time  # timestamp
        # self.version = version  # float
        # self.group_by = group_by  # string
        # self.ip = ip  # string

    # Note: this function only exists to provide an interface and abstract away from internal representation.
    def get_data(self):
        """returns a dict containing the data of the EndpointCall"""
        return self.data
