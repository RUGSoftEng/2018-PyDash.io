"""
Handles changing dashboard settings.
"""

from flask import jsonify, request
from flask_login import current_user

import pydash_app.dashboard
import pydash_app.dashboard.repository
import pydash_app.dashboard.services
import pydash_logger

logger = pydash_logger.Logger(__name__)


def change_dashboard_settings(dashboard_id):
    try:
        dashboard = pydash_app.dashboard.find(dashboard_id)
    except KeyError:
        logger.warning(f'Changing dashboard settings failed - {dashboard_id} not found')
        result = {'message': f'Could not find dashboard with id {dashboard_id}'}
        return jsonify(result), 404
    except ValueError:
        logger.warning(f'Changing dashboard settings failed - {dashboard_id} not a valid UUID')
        result = {'message': 'Invalid dashboard id'}
        return jsonify(result), 400

    if dashboard.user_id != current_user.id:
        logger.warning(f"{current_user} is not authorised to view {dashboard}")
        result = {"message": "Not authorised to view this dashboard"}
        return jsonify(result), 403

    settings = request.get_json(silent=True)

    if not settings:
        logger.warning('Changing dashboard settings failed - JSON settings object missing')
        result = {'message': 'Settings object missing'}
        return jsonify(result), 400

    settings_to_change = {}

    new_name = settings.get('name', dashboard.name)
    new_url = settings.get('url', dashboard.url)
    new_token = settings.get('token', dashboard.token)

    if not isinstance(new_name, str) or not isinstance(new_url, str) or not isinstance(new_token, str):
        logger.warning(f'Changing dashboard settings failed - invalid type of one or more settings: {settings}')
        result = {'message': 'Invalid value(s) provided for one or more dashboard settings'}
        return jsonify(result), 400

    if new_name != dashboard.name:
        settings_to_change['name'] = new_name

    if new_url != dashboard.url:
        is_valid, result = pydash_app.dashboard.services.is_valid_dashboard(new_url)
        if not is_valid:
            return jsonify(result), 400

        settings_to_change['url'] = new_url

    if new_token != dashboard.token:
        settings_to_change['token'] = new_token

    if len(settings_to_change) > 0:
        if 'name' in settings_to_change:
            dashboard.name = settings_to_change['name']

        if 'url' in settings_to_change:
            dashboard.url = settings_to_change['url']

        if 'token' in settings_to_change['url']:
            dashboard.token = settings_to_change['token']

        pydash_app.dashboard.repository.update(dashboard)

    logger.info('Successfully changed dashboard settings for {dashboard}')

    result = {
        'message': 'Successfully changed dashboard settings',
        'changed': [*settings_to_change]
    }
    return jsonify(result), 200
