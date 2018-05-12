"""
Performs the remote requests to the flask-monitoring-dashboard.

The method names in this module 1:1 reflect the names of the flask-monitoring-dashboard API
(but without the word 'JSON' in them, because conversion from JSON to Python dictionaries/lists
is one of the thing this module handles for you.)
"""

import requests, requests.exceptions
import jwt
import json

import pydash_logger

_DETAILS_ENDPOINT = 0
_RULES_ENDPOINT = 1
_DATA_ENDPOINT = 2

# In seconds
_REQUEST_TIMEOUT = 1

logger = pydash_logger.Logger(__name__)


def get_details(dashboard_url, timeout=_REQUEST_TIMEOUT):
    """
    Get details from a deployed flask-monitoring-dashboard
    :param dashboard_url: The base URL for the deployed dashboard, without trailing slash
    :param timeout: Optional timeout to wait for a response from the dashboard
    :return: A dict containing details from the dashboard, or None if the request was unsuccessful
    """
    endpoint = _endpoint_name(_DETAILS_ENDPOINT)

    try:
        response = requests.get(f'{dashboard_url}/{endpoint}', timeout=timeout)
    except requests.exceptions.ConnectionError as e:
        logger.error(f'Connection error in get_details: {e}')
        raise
    except requests.exceptions.Timeout as e:
        logger.error(f'Timeout error in get_details: {e}')
        raise

    if response.status_code != 200:
        logger.error(f'Bad response status code in get_details: {response.status_code}')
        response.raise_for_status()

    try:
        return json.loads(response.text)
    except json.JSONDecodeError:
        logger.error('Response to get_json_details contains malformed JSON')
        raise


def get_monitor_rules(dashboard_url, dashboard_token, timeout=_REQUEST_TIMEOUT):
    """
    Get monitor rules from a deployed flask-monitoring-dashboard
    :param dashboard_url: The base URL for the deployed dashboard, without trailing slash
    :param dashboard_token: The secret token for the dashboard, used to decode the Json Web Token response
    :param timeout: Optional timeout to wait for a response from the dashboard
    :return: A dict containing monitor rules of the dashboard, or None if the request was unsuccessful
    """
    endpoint = _endpoint_name(_RULES_ENDPOINT)

    try:
        response = requests.get(f'{dashboard_url}/{endpoint}', timeout=timeout)
    except requests.exceptions.ConnectionError as e:
        logger.error(f'Connection error in get_monitor_rules: {e}')
        raise
    except requests.exceptions.Timeout as e:
        logger.error(f'Timeout error in get_monitor_rules: {e}')
        raise

    if response.status_code != 200:
        logger.error(f'Bad response status code in get_monitor_rules: {response.status_code}')
        response.raise_for_status()

    return _decode_jwt(response.text, dashboard_token)


def get_data(dashboard_url, dashboard_token, time_from=None, time_to=None, timeout=_REQUEST_TIMEOUT):
    """
    Get data from a deployed flask-monitoring-dashboard
    :param dashboard_url: The base URL for the deployed dashboard, without trailing slash
    :param dashboard_token: The secret token for the dashboard, used to decode the Json Web Token response
    :param time_from: An optional datetime indicating only data since that moment should be included
    :param time_to: An optional datetime indicating only data up to that point should be included;
    only valid if time_from is also specified
    :param timeout: Optional timeout to wait for a response from the dashboard
    :return: A dict containing all monitoring data, possibly limited to the given time range
    """
    endpoint = _endpoint_name(_DATA_ENDPOINT)

    url = f'{dashboard_url}/{endpoint}'

    if time_from is None and time_to is not None:
        logger.error('Invalid input parameter combination: when time_from is None, time_to may not be specified.')
        raise ValueError('when time_from is None, time_to may not be specified')

    if time_from is not None:
        time_from = int(time_from.timestamp())
        url = f'{url}/{time_from}'
    if time_to is not None:
        time_to = int(time_to.timestamp())
        url = f'{url}/{time_to}'

    try:
        response = requests.get(url, timeout=timeout)
    except requests.exceptions.ConnectionError:
        logger.error(f'Connection error in get_data: {e}')
        raise
    except requests.exceptions.Timeout as e:
        logger.error(f'Timeout error in get_data: {e}')
        raise

    if response.status_code != 200:
        logger.error(f'Bad response status code in get_data: {response.status_code}')
        response.raise_for_status()

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
    try:
        message = jwt.decode(payload, token, algorithms=['HS256'])
        return json.loads(message['data'])
    except jwt.DecodeError as e:
        logger.error(f'While decoding: {e}\n'
                     f'JWT payload: {payload}')
        raise
    except KeyError:
        logger.error(f'After decoding: JWT-decoded message dict does not contain "data" entry')
        raise
    except json.JSONDecodeError:
        logger.error(f'After decoding: data entry of JWT-decoded message dict contains malformed JSON')
        raise
