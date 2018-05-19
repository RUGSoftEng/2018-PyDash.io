"""
Manages changing of the user's password.
"""

from flask import jsonify
from flask_login import current_user
from flask_restplus.reqparse import RequestParser

import pydash_app.user
import pydash_app.user.repository as user_repository
import pydash_logger

logger = pydash_logger.Logger(__name__)


def change_password():
    logger.info(f'Password change requested for {current_user}')

    args = _parse_arguments()

    if 'current_password' not in args or 'new_password' not in args:
        logger.warning('Password change failed - current password or new password missing')
        result = {'message': 'Current password or new password missing'}
        return jsonify(result), 400

    current_password = args['current_password']
    new_password = args['new_password']

    if not current_user.check_password(current_password):
        logger.warning('Password change failed - current password invalid')
        result = {'message': 'Current password incorrect'}
        return jsonify(result), 401

    actual_user = pydash_app.user.maybe_find_user(current_user.id)

    if not actual_user:
        logger.warning('Password change failed - current user does not exist for some reason')
        result = {'message': 'Current user does not exist'}
        return jsonify(result), 500

    try:
        actual_user.set_password(new_password)
    except ValueError:
        logger.warning("Password change failed - new password invalid")
        result = {'message': 'New password invalid'}
        return jsonify(result), 400

    user_repository.update(actual_user)

    result = {'message': 'Successfully changed password'}
    return jsonify(result), 200


def _parse_arguments():
    parser = RequestParser()
    parser.add_argument('current_password')
    parser.add_argument('new_password')
    return parser.parse_args()