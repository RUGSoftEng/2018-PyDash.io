from flask import jsonify
from flask_login import current_user
from flask_restplus.reqparse import RequestParser

import pydash_app.dashboard
import pydash_logger
import pydash_app.dashboard.services.fetching


logger = pydash_logger.Logger(__name__)


def register_dashboard():
    args = _parse_arguments()

    if not args['name'] or not args['url'] or not args['token']:
        logger.warning("Dashboard registration failed - name, url or token are missing.")
        result = {'message': 'Name, url or token are missing.'}
        return jsonify(result), 400

    logger.warning(f'{args}')

    name = args['name']
    url = args['url']
    token = args['token']

    is_valid, result = _is_valid_dashboard(url)
    if not is_valid:
        return jsonify(result), 400

    dashboard = pydash_app.dashboard.Dashboard(url, token, str(current_user.id), name)
    pydash_app.dashboard.add_to_repository(dashboard)
    message = {'message': 'Dashboard successfully registered to user.'}
    logger.info(f"Dashboard {name} ({url}) successfully registered to user {current_user.id} ")

    pydash_app.dashboard.services.fetching.schedule_historic_dashboard_fetching(dashboard)

    return jsonify(message), 200


def _parse_arguments():
    parser = RequestParser()
    parser.add_argument('name')
    parser.add_argument('url')
    parser.add_argument('token')
    return parser.parse_args()


def _is_valid_dashboard(url):
    import requests.exceptions
    import json
    import flask_monitoring_dashboard_client

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
