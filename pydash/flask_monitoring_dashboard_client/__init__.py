"""
Performs the remote requests to the flask-monitoring-dashboard.

The method names in this module 1:1 reflect the names of the flask-monitoring-dashboard API
(but without the word 'JSON' in them, because conversion from JSON to Python dictionaries/lists
is one of the thing this module handles for you.)
"""

import requests
import jwt
import json

import pydash_logger

DETAILS_ENDPOINT = 0
RULES_ENDPOINT = 1
DATA_ENDPOINT = 2

logger = pydash_logger.Logger(__name__)

def get_details(dashboard_url):
    """
    Get details from a deployed flask-monitoring-dashboard
    :param dashboard_url: The base URL for the deployed dashboard, without trailing slash
    :return: A dict containing details from the dashboard, or None if the request was unsuccessful
    """
    endpoint = _endpoint_name(DETAILS_ENDPOINT)

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
    endpoint = _endpoint_name(RULES_ENDPOINT)

    response = requests.get(f'{dashboard_url}/{endpoint}')

    if response.status_code != 200:
        return None

    return _decode_jwt(response.text, dashboard_token)


def get_data(dashboard_url, dashboard_token, time_from=None, time_to=None):
    """
    Get data from a deployed flask-monitoring-dashboard
    :param dashboard_url: The base URL for the deployed dashboard, without trailing slash
    :param dashboard_token: The secret token for the dashboard, used to decode the Json Web Token response
    :param time_from: An optional datetime indicating only data since that moment should be included
    :param time_to: An optional datetime indicating only data up to that point should be included
    :return: A dict containing all monitoring data or data since a given timestamp
    """
    endpoint = _endpoint_name(DATA_ENDPOINT)

    url = f'{dashboard_url}/{endpoint}'

    if time_from is None and time_to is not None:
        logger.error('Invalid input paramater combination: when time_from is None, time_to may not be specified.')
        return None

    if time_from is not None:
        time_from = int(time_from.timestamp())
        url = f'{url}/{time_from}'
    if time_to is not None:
        time_to = int(time_to.timestamp())
        url = f'{url}/{time_to}'

    response = requests.get(url)

    if response.status_code != 200:
        logger.error(f'Bad response status code: {response.status_code}')
        return None

    return _decode_jwt(response.text, dashboard_token)


def _endpoint_name(endpoint):
    names = [
        'get_json_details',
        'get_json_monitor_rules',
        'get_json_data'
    ]
    return names[endpoint]


def _decode_jwt(payload, token):
    """
    Decode a Json Web Token response from the python-monitoring-dashboard JSON data API
    :param payload: The JWT payload to decode
    :param token: The secret token for the dashboard
    :return: A dict containing the data from the payload
    """
    message = jwt.decode(payload, token, algorithms=['HS256'])
    return json.loads(message['data'])