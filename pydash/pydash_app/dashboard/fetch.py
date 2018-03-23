import requests
import jwt
import json


def get_details(dashboard_url):
    """
    Get details from a deployed flask-monitoring-dashboard
    :param dashboard_url: The base URL for the deployed dashboard, without trailing slash
    :return: A dict containing details from the dashboard, or None if the request was unsuccessful
    """
    endpoint = 'get_json_details'
    response = requests.get(f'{dashboard_url}/{endpoint}')

    if response.status_code != 200:
        return None

    return json.loads(response.text)


def get_monitor_rules(dashboard_url, dashboard_token):
    """
    Get monitor rules from a deployed flask-monitoring-dashboard
    :param dashboard_url: The base URL for the deployed dashboard, without trailing slash
    :param dashboard_token: The secret token for the dashboard, used to decode the Json Web Token response
    :return: A dict containing monitor rules of the dashboard, or None if the request was unsuccessful
    """
    endpoint = 'get_json_monitor_rules'
    response = requests.get(f'{dashboard_url}/{endpoint}')

    if response.status_code != 200:
        return None

    return _decode_jwt(response.text, dashboard_token)


def get_data(dashboard_url, dashboard_token, time_from=None):
    """
    Get data from a deployed flask-monitoring-dashboard
    :param dashboard_url: The base URL for the deployed dashboard, without trailing slash
    :param dashboard_token: The secret token for the dashboard, used to decode the Json Web Token response
    :param time_from: An optional timestamp string indicating only data since that timestamp should be included
    :return: A dict containing all monitoring data or data since a given timestamp
    """
    endpoint = 'get_json_data'
    url = f'{dashboard_url}/{endpoint}'
    if time_from is not None:
        url = f'{url}/{time_from}'

    response = requests.get(url)

    if response.status_code != 200:
        return None

    return _decode_jwt(response.text, dashboard_token)


def _decode_jwt(payload, token):
    """
    Decode a Json Web Token response from the python-monitoring-dashboard JSON data API
    :param payload: The JWT payload to decode
    :param token: The secret token for the dashboard
    :return: A dict containing the data from the payload
    """
    message = jwt.decode(payload, token, algorithms=['HS256'])
    return json.loads(message['data'])
