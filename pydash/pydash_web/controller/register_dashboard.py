from flask import jsonify
from flask_login import current_user
from flask_restplus.reqparse import RequestParser

import pydash_app.dashboard
import pydash_logger
import pydash_app.dashboard.services.fetching as fetching


logger = pydash_logger.Logger(__name__)


def register_dashboard():
    args = _parse_arguments()

    if not args['name'] or not args['url'] or not args['token']:
        logger.warning("Dashboard registration failed - name, url or token are missing.")
        result = {'message': 'Name, url or token are missing.'}
        return jsonify(result), 400

    logger.warning(f'{args}')

    name = str(args['name'])
    url = str(args['url'])
    token = str(args['token'])

    dashboard = pydash_app.dashboard.Dashboard(url, token, str(current_user.id), name)
    pydash_app.dashboard.add_to_repository(dashboard)
    message = {'message': 'Dashboard successfully registered to user.'}
    logger.info(f"Dashboard {name} ({url}) successfully registered to user {current_user.id} ")

    _schedule_dashboard_fetching(dashboard)

    return jsonify(message), 200


def _parse_arguments():
    parser = RequestParser()
    parser.add_argument('name')
    parser.add_argument('url')
    parser.add_argument('token')
    return parser.parse_args()


def _schedule_dashboard_fetching(dashboard):
    fetching.schedule_historic_dashboard_fetching(dashboard)
    fetching.schedule_periodic_dashboard_fetching(dashboard)
