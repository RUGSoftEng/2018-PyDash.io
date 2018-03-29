"""
Manages the lookup and returning of dashboard information for a certain user.

Currently only returns static mock data.
"""

from flask import jsonify


def dashboard(dashboard_id):
    """
    Lists information of a single dashboard.
    :param dashboard_id: ID of the dashboard to return.
    :return: A tuple containing:
             - A dict, containing the dashboard details of the current user's dashboards.
               or
               A dict containing an error message describing the particular error.
             - A corresponding HTML status code.

    Note: For now, this function only returns static mock data and the actual value of dashboard_id is ignored.
    """

    return jsonify(_json_mock_data()[0]), 200


# Currently returns mock-data.
def dashboards():
    """
    Lists the dashboards of the current user.
    :return: A tuple containing:
             - A list of dicts, containing dashboard details of the current user's dashboards.
               or
               A dict containing an error message describing the particular error.
             - A corresponding HTML status code.

    Note: For now, this function only returns static mock data.
    """

    dbs = _json_mock_data()
    return jsonify(dbs), 200


def _json_mock_data():
    """
    Returns mock data for the dashboard() and dashboards() API calls.
    :return: A list of dictionaries, each containing the details of a mock dashboard.
    """
    mock_data = [
                  {
                    "id": "4242424242424242",
                    "url": "http://pydash.io/",
                    "endpoints": [
                      {
                        "name": "my.endpoint.name",
                        "enabled": True
                      }
                    ]
                  },
                  {
                    "id": "5353535353535353",
                    "url": "http://pistach.io/",
                    "endpoints": [
                      {
                        "name": "my.other.endpoint.name",
                        "enabled": False
                      }
                    ]
                  }
                ]

    return mock_data
