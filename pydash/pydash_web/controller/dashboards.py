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

    return jsonify(_json_mock_dashboard_detail()), 200


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

    dbs = _json_mock_dashboards()
    return jsonify(dbs), 200


def _json_mock_dashboards():
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


def _json_mock_dashboard_detail():
    return {
        "id": "4242424242424242",
        "url": "http://pydash.io/",
        "aggregates": {
            "total_visits": _json_mock_total_visits(),
            "visits_per_day": _json_mock_visits_per_day()
        },
        "endpoints": [
            {
                "name": "my.endpoint.name",
                "enabled": True,
                # TODO: Highly possible that we'll move this to a separate dashboards/<dashboard_id>/endpoints/<endpoint_id> call in the future.
                "aggregates": {
                    "total_visits": _json_mock_total_visits(),
                    "visits_per_day": _json_mock_visits_per_day()
                },
            }
        ],
    }


from datetime import datetime, timedelta
def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)


def _json_mock_visits_per_day():
    fake_visits = [
        100,
        123,
        34,
        10,
        55,
        145,
        180,
        200,
        210,
        199,
        220,
        250,
        271,
        300,
    ]
    last_week = [_json_date(date) for date in daterange(datetime.today() - timedelta(days=len(fake_visits)), datetime.today())]
    return dict(zip(last_week, fake_visits))


def _json_mock_total_visits():
    return sum(_json_mock_visits_per_day().values())


def _json_date(datetime):
    """
    Returns dates in JS-compatible string format.
    (Only keeps the date-part.)
    """
    return datetime.strftime('%Y-%m-%d')
