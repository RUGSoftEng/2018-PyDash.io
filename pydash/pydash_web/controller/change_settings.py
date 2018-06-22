"""
Manages changing of user settings.
"""

from flask import request, jsonify
from flask_login import current_user
from email_validator import validate_email, EmailNotValidError

import pydash_app.user
import pydash_app.user.repository as user_repository
import pydash_logger


logger = pydash_logger.Logger(__name__)


def change_settings():
    logger.info(f'Settings change requested for {current_user}')

    # silent=True makes sure None is returned on failure
    # instead of calling Request.on_json_loading_failed()
    settings = request.get_json(silent=True)

    if not settings:
        logger.warning('Changing settings failed - JSON settings object missing')
        result = {'message': 'Changing settings failed - settings object missing'}
        return jsonify(result), 400

    settings_to_change = {}

    new_username = settings.get('username', current_user.name)
    new_sound_setting = settings.get('play_sounds', current_user.play_sounds)
    new_mail = settings.get('mail', current_user.mail)

    if not isinstance(new_username, str) or not isinstance(new_sound_setting, bool) or not isinstance(new_mail, str):
        logger.warning(f'Changing settings failed - invalid type of one or more settings: {settings}')
        result = {'message': 'Invalid value(s) provided for one or more settings'}
        return jsonify(result), 400

    # Username
    if new_username != current_user.name:
        if user_repository.find_by_name(new_username) is not None:
            logger.warning('Changing settings failed - new username already in use')
            result = {'message': 'Username already in use'}
            return jsonify(result), 400

        settings_to_change['name'] = new_username

    # Sound settings
    if new_sound_setting != current_user.play_sounds:
        settings_to_change['play_sounds'] = new_sound_setting

    # Email
    if new_mail != current_user.mail:

        if '@' not in new_mail:
                logger.warning(f"Changing settings failed - mail address invalid")
                result = {'message': 'Invalid mail address'}
                return jsonify(result), 400

        settings_to_change['mail'] = new_mail

    if len(settings_to_change) > 0:
        # Since current_user is not of the type pydash_app.user.entity.User, retrieve the actual user object
        actual_user = pydash_app.user.maybe_find_user(current_user.id)

        if not actual_user:
            logger.warning('Changing settings failed - current user does not exist for some reason')
            result = {'message': 'Current user does not exist'}
            return jsonify(result), 500

        if 'name' in settings_to_change:
            actual_user.name = settings_to_change['name']

        if 'play_sounds' in settings_to_change:
            actual_user.play_sounds = settings_to_change['play_sounds']

        if 'mail' in settings_to_change:
            actual_user.mail = settings_to_change['mail']

        user_repository.update(actual_user)

    logger.info('Successfully changed settings')

    result = {
        'message': 'Successfully changed settings',
        'changed': [*settings_to_change]
    }
    return jsonify(result), 200
