"""
Allows retrieval of dashboard downtime information.
"""

import datetime

from flask import jsonify
from flask_login import current_user

import pydash_app.dashboard
import pydash_logger

logger = pydash_logger.Logger(__name__)


def dashboard_downtime(dashboard_id):
    # TODO: accept variable date range

    try:
        dashboard = pydash_app.dashboard.find(dashboard_id)
    except KeyError:
        result = {'message': f'Dashboard_id {dashboard_id} is not found.'}
        logger.warning(f'Dashboard downtime failure - Dashboard_id {dashboard_id} is not found. '
                       f'Current user: {current_user}')
        return jsonify(result), 400
    except ValueError:  # Happens when called without a proper UUID
        result = {'message': f'Dashboard_id {dashboard_id} is invalid UUID.'}
        logger.warning(f'Dashboard downtime failure - Dashboard_id {dashboard_id} is invalid UUID. '
                       f'Current user: {current_user}')
        return jsonify(result), 400

    if str(dashboard.user_id) != str(current_user.id):
        result = {'message': f'Current user is not allowed to access dashboard {dashboard_id}'}
        logger.warning(f'Dashboard downtime failure - '
                       f'User {current_user} is not allowed to access dashboard {dashboard_id}')
        return jsonify(result), 403

    logger.info(f'Dashboard downtime successful for {dashboard}')

    result = _render_downtime_data(dashboard)

    return jsonify(result), 200


def _render_downtime_data(dashboard):
    data = dashboard.get_downtime_data()

    return {
        'downtime_intervals': {
            date: [_render_interval(interval) for interval in intervals]
            for (date, intervals) in data['downtime_intervals'].items()
        },
        'downtime_percentage': data['downtime_percentage'],
        'precise_downtimes': {
            date: _render_timedelta(delta)
            for (date, delta) in data['total_downtimes'].items()
        },
        'hour_downtimes': {
            date: delta / datetime.timedelta(hours=1)
            for (date, delta) in data['total_downtimes'].items()
        }
    }


def _render_interval(interval):
    return interval[0].isoformat(), interval[1].isoformat()


def _render_timedelta(delta):
    try:
        hours, remainder = divmod(delta.total_seconds(), 3600)
        minutes, seconds = divmod(remainder, 60)
    except AttributeError:
        hours = 0
        minutes = 0
        seconds = 0

    try:
        microseconds = delta.microseconds
    except AttributeError:
        microseconds = 0

    return {
        'hours': hours,
        'minutes': minutes,
        'seconds': seconds,
        'microseconds': microseconds
    }