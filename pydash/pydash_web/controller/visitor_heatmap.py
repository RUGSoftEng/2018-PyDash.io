from flask import jsonify, request
from datetime import timedelta, date, datetime
from pydash_app.dashboard import find_verified_dashboard

import pydash_logger


logger = pydash_logger.Logger(__name__)


def visitor_heatmap(dashboard_id, field='total_visits'):

    # Check dashboard_id
    valid_dashboard, result, http_error = find_verified_dashboard(dashboard_id)

    if not valid_dashboard:
        return result, http_error

    params = request.args

    if not params:
        logger.info('Visitor_heatmap - no datetime info specified.')
        result = {'message': 'Visitor_heatmap failure - datetime info missing'}
        return jsonify(result), 400

    # Get datetime info
    start_date = params['start_date']
    end_date = params.get('end_date')

    if not start_date:
        logger.info('Visitor_heatmap - no datetime start_date specified.')
        result = {'message': 'Visitor_heatmap failure - datetime start_date missing'}
        return jsonify(result), 400

    # Now generate date classes for each
    start_date = start_date.split('-')
    start_date = date(int(start_date[0]), int(start_date[1]), int(start_date[2]))

    if not end_date:
        # use current date if none provided
        end_date = datetime.today().strftime('%Y-%m-%d')

    end_date = end_date.split('-')
    end_date = date(int(end_date[0]), int(end_date[1]), int(end_date[2]))

    # Generate list for each day that contains all the hourly data.
    data = [get_hourly_data(valid_dashboard, single_date, field) for single_date in daterange(start_date, end_date)]

    logger.info(f"visitor_heatmap successful - data from dashboard {dashboard} requested")

    return jsonify(data), 200


def get_hourly_data(dashboard, day, field):

    # Gets a list of data per hour of the day.
    return [dashboard._aggregator_group.fetch_aggregator({'hour': str(day) + 'T' + str(i)}).as_dict()[str(field)]
            for i in range(0, 23)]


def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)
