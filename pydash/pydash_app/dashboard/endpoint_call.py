
import persistent


class EndpointCall(persistent.Persistent):
    """
    EndpointCall entities only serve to store JSON data pulled from the external dashboards.

    As with the other entity classes, it does not concern itself with the implementation of its persistence,
    as it doesn't exist on its own.
    If this were the case, the `endpointcall_repository` would handle this concern.
    """

    def __init(self, endpoint, execution_time, time, version, group_by, ip):
        """
        TODO: Add this description.
        :param endpoint: String denoting the endpoint's name.
        :param execution_time: Float denoting the execution time of the endpoint call.
        :param time: Timestamp denoting the time the endpoint call was made.
        :param version: Float (?) denoting the dashboard's version number.
        :param group_by: String denoting the category # TODO: complete this.
        :param ip: String denoting the IP-address the endpoint call was made from.
        """
        self.endpoint = endpoint  # string
        self.execution_time = execution_time  # float
        self.time = time  # timestamp
        self.version = version  # float
        self.group_by = group_by  # string
        self.ip = ip  # string
