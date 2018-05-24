"""
Contains services for the 'Dashboard' concern.

These are things that use or manipulate 'Dashboard' entities to perform tasks,
where these tasks are either too complex to put in the Dashboard Entity,
or where these are heavily interacting with outside logic that the business domain entity should not concern itself with directly.
"""

import requests.exceptions
import json
import flask_monitoring_dashboard_client


def is_valid_dashboard(url):
    try:
        details = flask_monitoring_dashboard_client.get_details(url)
        version = details['dashboard-version']
    except requests.exceptions.ConnectionError:
        return False, {'message': 'Could not connect to the dashboard'}
    except requests.exceptions.Timeout:
        return False, {'message': 'Timeout while connecting to the dashboard'}
    except requests.exceptions.HTTPError as e:
        if e.response:
            return False, {'message': f'HTTP {e.response.status_code} error while connecting to the dashboard'}
        return False, {'message': 'HTTP error while connecting to the dashboard'}
    except json.JSONDecodeError:
        return False, {'message': f'{url} does not seem to host a valid dashboard'}
    except KeyError:
        return False, {'message': 'Unsupported version of Flask-MonitoringDashboard'}
    except requests.exceptions.RequestException:
        return False, {'message': f'{url} seems to be an invalid url'}

    return True, None
