import persistent
from datetime import datetime


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
        :param time: datetime.datetime object denoting the time the endpoint call was made.
        :param version: String denoting the dashboard's version number.
        :param group_by: String denoting which user is calling the function (?).
        :param ip: String denoting the IP-address the endpoint call was made from.
        """
        EndpointCall.__check_arg_types(endpoint, execution_time, time, version, group_by, ip)

        self.endpoint = endpoint  # string
        self.execution_time = execution_time  # float
        self.time = time  # datetime.datetime
        self.version = version  # string
        self.group_by = group_by  # string
        self.ip = ip  # string

    def __repr__(self):
        """
        Returns a string representation of this EndpointCall, for easy debugging and logging:

            >>> EndpointCall("foo", 0.5, datetime.strptime("2018-04-25 15:29:23", "%Y-%m-%d %H:%M:%S"), "0.1", "None", "127.0.0.1")
            <EndpointCall
                endpoint=foo
                execution_time=0.5
                time=2018-04-25 15:29:23
                version=0.1
                group_by=None
                ip=127.0.0.1
            >

        """
        return f'''<{self.__class__.__name__}
    endpoint={self.endpoint}
    execution_time={self.execution_time}
    time={self.time}
    version={self.version}
    group_by={self.group_by}
    ip={self.ip}
>'''


    @staticmethod
    def __check_arg_types(endpoint, execution_time, time, version, group_by, ip):
        if not isinstance(endpoint, str):
            raise TypeError('EndpointCall expects endpoint to be a string.')
        if not isinstance(execution_time, float):
            raise TypeError('EndpointCall expects execution_time to be a float.')
        if not isinstance(time, datetime):
            raise TypeError('EndpointCall expects time to be a datetime.')
        if not isinstance(version, str):
            raise TypeError('EndpointCall expects version to be a string.')
        if not isinstance(group_by, str):
            raise TypeError('EndpointCall expects group_by to be a string.')
        if not isinstance(ip, str):
            raise TypeError('EndpointCall expects ip to be a string.')

    # Note: this function only exists to provide an interface and abstract away from internal representation.
    def as_dict(self):
        """returns a dict containing the data of the EndpointCall"""
        return {"endpoint": self.endpoint,
                "execution_time": self.execution_time,
                "time": self.time,
                "version": self.version,
                "group_by": self.group_by,
                "ip": self.ip
            }
