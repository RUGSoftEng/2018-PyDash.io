from flask import jsonify, request
from flask_login import current_user
from datetime import timedelta, date, datetime

import pydash_app.dashboard
import pydash_logger
import pydash_app.dashboard.services


logger = pydash_logger.Logger(__name__)


def visitor_heatmap(dashboard_id, field='total_visits'):

    # Check dashboard_id
    # TODO get this slice of code out of here since it is in multiple controller methods
    try:
        dashboard = pydash_app.dashboard.find(dashboard_id)
    except KeyError:
        result = {'message': f'Dashboard_id {dashboard_id} is not found.'}
        logger.warning(f'Endpoint_boxplots failure - Dashboard_id {dashboard_id} is not found. '
                       f'Current user: {current_user}')
        return jsonify(result), 400
    except ValueError:  # Happens when called without a proper UUID
        result = {'message': f'Dashboard_id {dashboard_id} is invalid UUID.'}
        logger.warning(f'Endpoint_boxplots failure - Dashboard_id {dashboard_id} is invalid UUID. '
                       f'Current user: {current_user}')
        return jsonify(result), 400

    # Check user authorisation
    if str(dashboard.user_id) != str(current_user.id):
        result = {'message': f'Current user is not allowed to access dashboard {dashboard_id}'}
        logger.warning(f'Endpoint_boxplots failure - '
                       f'User {current_user} is not allowed to access dashboard {dashboard_id}')
        return jsonify(result), 403

    # silent=True makes sure None is returned on failure
    # instead of calling Request.on_json_loading_failed()
    params = request.get_json(silent=True)

    if not params:
        logger.info('Visitor_heatmap - no datetime info specified.')
        result = {'message': 'Visitor_heatmap failure - datetime info missing'}
        return jsonify(result), 400

    # Get datetime info
    start_date = params['start_date', None]
    end_date = params.get('end_date', None)

    if not start_date:
        logger.info('Visitor_heatmap - no datetime start_date specified.')
        result = {'message': 'Visitor_heatmap failure - datetime start_date missing'}
        return jsonify(result), 400

    # Now generate date classes for each
    start_date = start_date.split('-')
    start_date = date(int(start_date[0]), int(start_date[1]), int(start_date[2]))
    # start_date.strftime('%Y-%m-%d')  # NOTE: seems to have no effect

    if not end_date:
        # use current date if none provided
        end_date = datetime.today().strftime('%Y-%m-%d')
    else:
        end_date = end_date.split('-')

    end_date = date(int(end_date[0]), int(end_date[1]), int(end_date[2]))

    # Generate list for each day that contains all the hourly data.
    data = [get_hourly_data(dashboard, single_date, field) for single_date in daterange(start_date, end_date)]

    logger.info(f"visitor_heatmap successful - data from dashboard {dashboard} requested")

    return jsonify(data), 200


def get_hourly_data(dashboard, day, field):

    # Gets a list of data per hour of the day.
    return [dashboard._aggregator_group.fetch_aggregator({'hour': str(day) + 'T' + str(i)}).as_dict()[str(field)]
            for i in range(0, 23)]


def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)
