"""
Handles changing dashboard settings.
"""

from flask import jsonify, request

import pydash_app.dashboard
import pydash_app.dashboard.repository
import pydash_app.dashboard.services
import pydash_logger

logger = pydash_logger.Logger(__name__)


def change_dashboard_settings(dashboard_id):

    # Check dashboard_id
    valid_dashboard, result, http_error = pydash_app.dashboard.find_verified_dashboard(dashboard_id)

    if not valid_dashboard:
        return result, http_error

    settings = request.get_json(silent=True)

    if not settings:
        logger.warning('Changing dashboard settings failed - JSON settings object missing')
        result = {'message': 'Settings object missing'}
        return jsonify(result), 400

    settings_to_change = {}

    new_name = settings.get('name', valid_dashboard.name)
    new_url = settings.get('url', valid_dashboard.url)
    new_token = settings.get('token', valid_dashboard.token)

    if not isinstance(new_name, str) or not isinstance(new_url, str) or not isinstance(new_token, str):
        logger.warning(f'Changing dashboard settings failed - invalid type of one or more settings: {settings}')
        result = {'message': 'Invalid value(s) provided for one or more dashboard settings'}
        return jsonify(result), 400

    if new_name != valid_dashboard.name:
        settings_to_change['name'] = new_name

    if new_url != valid_dashboard.url:
        is_valid, result = pydash_app.dashboard.services.is_valid_dashboard(new_url)
        if not is_valid:
            return jsonify(result), 400

        settings_to_change['url'] = new_url

    if new_token != valid_dashboard.token:
        settings_to_change['token'] = new_token

    if len(settings_to_change) > 0:
        if 'name' in settings_to_change:
            valid_dashboard.name = settings_to_change['name']

        if 'url' in settings_to_change:
            valid_dashboard.url = settings_to_change['url']

        if 'token' in settings_to_change['url']:
            valid_dashboard.token = settings_to_change['token']

        pydash_app.dashboard.repository.update(valid_dashboard)

    logger.info(f'Successfully changed dashboard settings for {valid_dashboard}')

    result = {
        'message': 'Successfully changed dashboard settings',
        'changed': [*settings_to_change]
    }
    return jsonify(result), 200
