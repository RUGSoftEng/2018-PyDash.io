"""
Manages the lookup and returning of dashboard information for a certain user.

Currently only returns static mock data.
"""

from flask import jsonify
from flask_login import current_user

import pydash_app.dashboard


def dashboard(dashboard_id):
    """
    Lists information of a single dashboard.
    :param dashboard_id: ID of the dashboard to return.
    :return: A tuple containing:
             - A dict, containing the dashboard details of the current user's dashboards.
               or
               A dict containing an error message describing the particular error.
             - A corresponding HTML status code.
    """
    try:
        db = pydash_app.dashboard.find(dashboard_id)
    except KeyError:
        return jsonify({"message": "Could not find a matching dashboard."}), 404
    except ValueError: # Happens when called without a proper UUID -- return test data for now in this case.
        return jsonify(_json_mock_dashboard_detail())

    if db.user_id != current_user.id:
        return jsonify({"message": "Not authorised to view this dashboard."}), 403

    return jsonify(_dashboard_detail(db)), 200


def dashboards():
    """
    Lists the dashboards of the current user.
    :return: A tuple containing:
             - A list of dicts, containing dashboard details of the current user's dashboards.
               or
               A dict containing an error message describing the particular error.
             - A corresponding HTML status code.
    """
    dbs = pydash_app.dashboard.dashboards_of_user(current_user.id)

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
    return jsonify(mock_data), 200


def _dashboard_detail(db):
    """
    Returns the representation of the given dashboard in detail.
    :param db: The Dashboard-entity in question.
    :return: A dict structured as the JSON-representation of the given dashboard.
    """

    return _json_mock_dashboard_detail()

def _json_mock_dashboard_detail():
    from pydash_app.dashboard.dashboard import Dashboard
    from pydash_app.dashboard.endpoint import Endpoint
    from pydash_app.dashboard.endpoint_call import EndpointCall
    import uuid
    from datetime import datetime, timedelta
    d = Dashboard("http://foo.io", str(uuid.uuid4()))
    e1 = Endpoint("foo", True)
    e2 = Endpoint("bar", True)
    d.add_endpoint(e1)
    d.add_endpoint(e2)
    ec1 = EndpointCall("foo", 0.5, datetime.now(), 0.1, "None", "127.0.0.1")
    ec2 = EndpointCall("foo", 0.1, datetime.now(), 0.1, "None", "127.0.0.2")
    ec3 = EndpointCall("bar", 0.2, datetime.now(), 0.1, "None", "127.0.0.1")
    ec4 = EndpointCall("bar", 0.2, datetime.now() - timedelta(days=1), 0.1, "None", "127.0.0.1")
    ec5 = EndpointCall("bar", 0.2, datetime.now() - timedelta(days=2), 0.1, "None", "127.0.0.1")
    ec6 = EndpointCall("bar", 0.2, datetime.now() - timedelta(days=3), 0.1, "None", "127.0.0.2")
    ec6b = EndpointCall("bar", 0.2, datetime.now() - timedelta(days=3), 0.1, "None", "127.0.0.2")
    ec6c = EndpointCall("bar", 0.2, datetime.now() - timedelta(days=3), 0.1, "None", "127.0.0.2")
    ec6d = EndpointCall("bar", 0.2, datetime.now() - timedelta(days=3), 0.1, "None", "127.0.0.2")
    ec7 = EndpointCall("bar", 0.3, datetime.now() - timedelta(days=5), 0.1, "None", "127.0.0.1")
    ec8 = EndpointCall("bar", 0.1, datetime.now() - timedelta(days=4), 0.1, "None", "127.0.0.2")
    d.add_endpoint_call(ec1)
    d.add_endpoint_call(ec2)
    d.add_endpoint_call(ec3)
    d.add_endpoint_call(ec4)
    d.add_endpoint_call(ec5)
    d.add_endpoint_call(ec6)
    d.add_endpoint_call(ec6b)
    d.add_endpoint_call(ec6c)
    d.add_endpoint_call(ec6d)
    d.add_endpoint_call(ec7)

    for n in range(0, 150):
        d.add_endpoint_call(EndpointCall("foo", n / 10, datetime.now() - timedelta(days = (n % 13)), 0.1, "None", "127.0.0.3"))

    aggregate_data = d.aggregated_data()
    # d.endpoints['foo'].aggregated_data()
    # d.endpoints['bar'].aggregated_data()
    def endpoint_dict(endpoint):
        return {
            'name': endpoint.name,
            'aggregates': endpoint.aggregated_data(),
            'enabled': endpoint.is_monitored
        }

    endpoints_dict = [endpoint_dict(endpoint) for endpoint in d.endpoints.values()]
    return {
        'id': d.id,
        'url': d.url,
        'aggregates': d.aggregated_data(),
        'endpoints': endpoints_dict
    }
