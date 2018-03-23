"""
Manages the lookup and returning of dashboard information for a certain user.

Currently only returns static mock data.
"""

from flask import jsonify


# Currently returns mock-data.
def get_dashboard(dashboard_id):

    return jsonify(__read_json_mock_data(0)), 200


# Currently returns mock-data.
def get_dashboards():
    dashboards = [__read_json_mock_data(0), __read_json_mock_data(1)]
    return jsonify(dashboards), 200


# Returns some static json mock data, for testing purposes
def __read_json_mock_data(index):
    return  [
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
                "url": "http://pydash.io/",
                "endpoints": [
                  {
                    "name": "my.other.endpoint.name",
                    "enabled": False
                  }
                ]
              }
            ][index]
