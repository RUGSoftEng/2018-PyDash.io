"""
Manages the lookup and returning of dashboard information for a certain user.

Currently only returns static mock data.
"""

from flask import jsonify
from flask_restplus.reqparse import RequestParser


#
def get_dashboard(dashboard_id):

    return jsonify(__read_json_mock_data()), 200


# Currently not yet implemented.
def get_dashboards():

    return jsonify({"message": "Not yet implemented."}), 501  # Currently not yet implemented.

    args = __parse_arguments()

    if 'dashboard_id' not in args:
        message = {"message": "Dashboard_id is missing."}
        return jsonify(message), 400

    # dashboards =

    return


def __parse_arguments():
    parser = RequestParser()
    parser.add_argument('dashboard_id')
    return parser.parse_args()


# Returns some static json mock data, for testing purposes
def __read_json_mock_data():
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
              }
            ]
