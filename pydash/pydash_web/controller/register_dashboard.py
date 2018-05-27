from flask import jsonify, request
from flask_login import current_user

import pydash_logger
import pydash_app.dashboard
import pydash_app.dashboard.services
import pydash_app.dashboard.services.fetching

logger = pydash_logger.Logger(__name__)


def register_dashboard():
    request_data = request.get_json(silent=True)

    if not request_data:
        logger.warning('Dashboard registration failed - data missing')
        result = {'message': 'Data missing'}
        return jsonify(result), 400

    name = request_data.get('name')
    url = request_data.get('url')
    token = request_data.get('token')

    if url is None or token is None:
        logger.warning("Dashboard registration failed - url or token are missing.")
        result = {'message': 'Name, url or token are missing.'}
        return jsonify(result), 400

    # In case name is '' or None (since name is optional)
    if not name:
        name = None

    is_valid, result = pydash_app.dashboard.services.is_valid_dashboard(url)
    if not is_valid:
        return jsonify(result), 400

    dashboard = pydash_app.dashboard.Dashboard(url, token, str(current_user.id), name)
    pydash_app.dashboard.add_to_repository(dashboard)
    message = {'message': 'Dashboard successfully registered to user.'}
    logger.info(f"Dashboard {name} ({url}) successfully registered to user {current_user.id} ")

    pydash_app.dashboard.services.fetching.schedule_historic_dashboard_fetching(dashboard)

    return jsonify(message), 200

