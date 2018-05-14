"""
Manages changing of user settings.
"""

from flask import request, jsonify
from flask_login import current_user

import pydash_app.user.repository as user_repository
import pydash_logger


logger = pydash_logger.Logger(__name__)


def change_settings():
    logger.info(f'Settings change requested for {current_user}')

    # silent=True makes sure None is returned on failure
    # instead of calling Request.on_json_loading_failed()
    settings = request.get_json(silent=True)

    if settings is None:
        logger.warning('Changing settings failed - JSON settings object missing')
        result = {'message': 'Settings object missing'}
        return jsonify(result), 400

    settings_to_change = {}

    new_username = settings.get('username', current_user.name)
    new_sound_setting = settings.get('play_sounds', current_user.play_sounds)

    if not isinstance(new_username, str) or not isinstance(new_sound_setting, bool):
        logger.warning(f'Changing settings failed - invalid type of one or more settings: {settings}')
        result = {'message': 'Invalid value(s) provided for one or more settings'}
        return jsonify(result), 400

    if new_username != current_user.name:
        if user_repository.find_by_name(new_username) is not None:
            logger.warning('Changing settings failed - new username already in use')
            result = {'message': 'Username already in use'}
            return jsonify(result), 400

        settings_to_change['name'] = new_username

    if new_sound_setting != current_user.play_sounds:
        settings_to_change['play_sounds'] = new_sound_setting

    if len(settings_to_change) > 0:
        for setting, value in settings_to_change.items():
            setattr(current_user, setting, value)

        user_repository.update(current_user)

    logger.info('Successfully changed settings')

    result = {
        'message': 'Successfully changed settings',
        'changed': [*settings_to_change]
    }
    return jsonify(result), 200
