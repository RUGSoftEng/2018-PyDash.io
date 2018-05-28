"""
Manages the lookup and returning of dashboard information for a certain user.

Currently only returns static mock data.
"""

from flask import jsonify, request
from flask_login import current_user

from datetime import datetime, timedelta, timezone
from copy import copy

import pydash_app.dashboard
from pydash_app.dashboard.aggregator import Aggregator
import pydash_logger

logger = pydash_logger.Logger(__name__)

datetime_formats = {'year': '%Y'}
datetime_formats['month'] = datetime_formats['year'] + '-%m'
datetime_formats['week'] = datetime_formats['year'] + '-W%W'
datetime_formats['day'] = datetime_formats['month'] + '-%d'
datetime_formats['hour'] = datetime_formats['day'] + 'T%H'
datetime_formats['minute'] = datetime_formats['hour'] + '-%M'


def dashboard(dashboard_id):
    """
    Lists information of a single dashboard.
    :param dashboard_id: ID of the dashboard to return.
    :return: A tuple containing:
             - A dict, containing the dashboard details of the current user's dashboards.
               or
               A dict containing an error message describing the particular error.
             - A corresponding HTML status code.
    """
    # Check dashboard_id
    valid_dashboard, result, http_error = pydash_app.dashboard.find_verified_dashboard(dashboard_id)

    if not valid_dashboard:
        return result, http_error

    params = request.args
    statistic = params.get('statistic')
    start_date = params.get('start_date', default='1970-1-1')
    end_date = params.get('end_date', default=datetime.utcnow().strftime('%Y-%m-%d %H-%M-%S'))
    timeslice = params.get('timeslice')

    if not statistic:  # Default to returning the generic dashboard_detail.
        logger.info(f"Retrieved dashboard {valid_dashboard}")
        return jsonify(_dashboard_detail(valid_dashboard)), 200
    else:

        start_date = match_datetime_string_with_formats(start_date)
        if start_date is None:
            logger.warning('In dashboard: Invalid format of start_date.')
            result = {"message": "Invalid format of start_date."}
            return jsonify(result), 400

        end_date = match_datetime_string_with_formats(end_date)
        if end_date is None:
            logger.warning('In dashboard: Invalid format of end_date.')
            result = {"message": "Invalid format of end_date."}
            jsonify(result), 400

        if not check_allowed_statistics(statistic):
            logger.warning(f'In dashboard: Statistic {statistic} is not supported for use.')
            result = {'message': f'Statistic {statistic} is not supported for use.'}
            return jsonify(result), 400

        if not timeslice:  # We are dealing with statistics that only deal with single aggregates, not multiple.
            result = handle_statistic_without_timeslice(valid_dashboard, statistic, start_date, end_date)
        else:
            if not check_allowed_timeslices(timeslice):
                logger.warning(f'In dashboard: Timeslice {timeslice} is not supported.')
                result = {'message': f'Timeslice {timeslice} is not supported.'}
                return jsonify(result), 400
            # Handle timeslice statistics
            result = handle_statistic_per_timeslice(valid_dashboard, statistic, timeslice, start_date, end_date)

        logger.info(f'Successfully handled dashboard-statistic call.'
                    f' statistic={statistic}, timeslice={timeslice}, start_date={start_date}, end_date={end_date}')
        return jsonify(result), 200


def handle_statistic_without_timeslice(dashboard, statistic, start_datetime, end_datetime):
    """
    These datetimes are treated as inclusive boundaries of a datetime range (e.g. [start_datetime, end_datetime]
    :param dashboard:
    :param statistic:
    :param start_datetime:
    :param end_datetime:
    :return: The value of a single statistic over the specified datetime range.
    """
    aggregator = dashboard.aggregated_data_daterange(start_datetime, end_datetime)
    return aggregator.as_dict()[statistic]


def handle_statistic_per_timeslice(dashboard, statistic, timeslice, start_datetime, end_datetime):
    """These datetimes are treated as inclusive boundaries of a datetime range (e.g. [start_datetime, end_datetime].
    Assumes start_timedate and end_timedate are both timezone aware, with timezone utc.
    :param dashboard:
    :param statistic:
    :param timeslice:
    :param start_datetime:
    :param end_datetime:
    :return: A list of tuples consisting of a datetime string (formatted in the following way: TODO: Write down format)
             and the corresponding statistic, over the specified datetime range.
    """
    statistics = []

    begin_timestamp = start_datetime.timestamp()
    end_timestamp = (end_datetime + timedelta(minutes=1)).timestamp()

    timeslice_increment_funcs = {'minute': lambda datetime_value : 60}
    timeslice_increment_funcs['hour'] = lambda datetime_value : timeslice_increment_funcs['minute'](datetime_value) * 60
    timeslice_increment_funcs['day'] = lambda datetime_value : timeslice_increment_funcs['hour'](datetime_value) * 24
    timeslice_increment_funcs['week'] = lambda datetime_value : timeslice_increment_funcs['hour'](datetime_value) * 7
    timeslice_increment_funcs['month'] = \
        lambda datetime_value : (datetime(datetime_value.year, datetime_value.month+1, datetime_value.day, datetime_value.hour,
                                          datetime_value.minute, datetime_value.second, tzinfo=timezone.utc)
                                 - datetime_value).total_seconds()
    timeslice_increment_funcs['year'] = \
        lambda datetime_value : (datetime(datetime_value.year+1, datetime_value.month, datetime_value.day, datetime_value.hour,
                                          datetime_value.minute, datetime_value.second, tzinfo=timezone.utc)
                                 - datetime_value).total_seconds()

    current_timestamp = copy(begin_timestamp)
    while current_timestamp < end_timestamp:
        delta_seconds = timeslice_increment_funcs[timeslice](datetime.fromtimestamp(current_timestamp))
        start = datetime.fromtimestamp(current_timestamp, tz=timezone.utc)
        end = start + timedelta(seconds=delta_seconds)
        current_timestamp += delta_seconds
        statistic_value = (datetime.fromtimestamp(current_timestamp, tz=timezone.utc).strftime(datetime_formats[timeslice]),
                           dashboard.aggregated_data_daterange(start, end)[statistic])
        statistics.append(statistic_value)

    return statistics


def match_datetime_string_with_formats(datetime_string):
    """Returns a datetime object if the provided string matched with one of the allowed formats
       Otherwise, returns None."""
    formats = ['%Y-%m-%d', '%Y-%m-%d %H-%M-%S']
    datetime_object = None
    for i in range(len(formats)):
        try:
            datetime_object = datetime.strptime(datetime_string, formats[i])
        except ValueError:
            continue
    return datetime_object


def check_allowed_timeslices(timeslice):
    return timeslice in ['year', 'month', 'week', 'day', 'hour', 'minute']


# def check_allowed_timeslice_statistics(statistic):
#     return statistic in ['visits_per_time', 'unique_visits_per_time', ]


def check_allowed_statistics(statistic):
    return statistic in ['total_visits', 'total_execution_time', 'average_execution_time', 'visits_per_ip',
                         'unique_visitors', 'fastest_measured_execution_time', 'fastest_quartile_execution_time',
                         'median_execution_time', 'slowest_quartile_execution_time', 'ninetieth_percentile_execution_time',
                         'ninety-ninth_percentile_execution_time', 'slowest_measured_execution_time']
#     or perhaps
#     return statistic in Aggregator().as_dict().keys()
#     if we prune all currently rendered statistics that can be retrieved otherwise.


def dashboards():
    """
    Lists the dashboards of the current user.
    :return: A tuple containing:
             - A list of dicts, containing dashboard details of the current user's dashboards.
               or
               A dict containing an error message describing the particular error.
             - A corresponding HTML status code.
    """
    logger.info(f"Retrieving list of dashboards for {current_user}")
    dashboards = pydash_app.dashboard.dashboards_of_user(current_user.id)

    return jsonify([_simple_dashboard_detail(dashboard) for dashboard in dashboards]), 200


def _simple_dashboard_detail(dashboard):
    """
    Returns a simple representation of the given dashboard.
    :param dashboard: The Dashboard-entity in question.
    :return: A dict structured as the simple JSON-representation of the given dashboard.
    """

    def endpoint_dict(endpoint):
        return {
            'name': endpoint.name,
            'enabled': endpoint.is_monitored
        }

    endpoints = [endpoint_dict(endpoint) for endpoint in dashboard.endpoints.values()]

    dashboard_data = {
        'id': dashboard.id,
        'url': dashboard.url,
        'name': dashboard.name,
        'error': dashboard.error,
        'endpoints': endpoints
    }

    return dashboard_data


def _dashboard_detail(dashboard):
    """
    Returns the representation of the given dashboard in detail.
    :param dashboard: The Dashboard-entity in question.
    :return: A dict structured as the JSON-representation of the given dashboard.
    """

    def endpoint_dict(endpoint):
        return {
            'name': endpoint.name,
            'aggregates': endpoint.aggregated_data(),
            'enabled': endpoint.is_monitored
        }

    endpoints = [endpoint_dict(endpoint) for endpoint in dashboard.endpoints.values()]

    dashboard_data = {
        'id': dashboard.id,
        'url': dashboard.url,
        'name': dashboard.name,
        'error': dashboard.error,
        'aggregates': dashboard.aggregated_data(),
        'endpoints': endpoints
    }

    return dashboard_data
