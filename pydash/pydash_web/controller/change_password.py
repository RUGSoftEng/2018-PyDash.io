"""
Manages changing of the user's password.
"""

from flask import jsonify, request
from flask_login import current_user

import pydash_app.user.repository as user_repository
import pydash_logger

logger = pydash_logger.Logger(__name__)


def change_password():
    logger.info(f'Password change requested for {current_user}')

    args = _parse_arguments()

    current_password = request.args.get('current_password')
    new_password = request.args.get('new_password')

    if current_password is None or new_password is None:
        logger.warning('Password change failed - current password or new password missing')
        result = {'message': 'Current password or new password missing'}
        return jsonify(result), 400

    if not current_user.check_password(current_password):
        logger.warning('Password change failed - current password invalid')
        result = {'message': 'Current password incorrect'}
        return jsonify(result), 401

    if not new_password:
        logger.warning('Password change failed - new password cannot be empty')
        result = {'message': 'New password cannot be empty'}
        return jsonify(result), 400

    current_user.set_password(new_password)
    user_repository.update(current_user)

    result = {'message': 'Successfully changed password'}
    return jsonify(result), 200