"""
Manages the lookup and returning of dashboard information for a certain user.

Currently only returns static mock data.
"""

from flask import jsonify, request
from flask_login import current_user

from datetime import datetime
from pydash_app.dashboard.aggregator.aggregator_group import allowed_timeslices
from pydash_app.dashboard.aggregator import Aggregator


import pydash_app.dashboard
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
    :param dashboard_id: ID of the dashboard to retrieve information from.
    :return: The returned value consists of a tuple of dashboard information, together with a http status code.
    This route supports the following request arguments:
    - statistic: The name of the statistic of which aggregated information should be returned.
      The currently supported statistics are:['total_visits', 'total_execution_time', 'average_execution_time', 'visits_per_ip',
                         'unique_visitors', 'fastest_measured_execution_time', 'fastest_quartile_execution_time',
                         'median_execution_time', 'slowest_quartile_execution_time', 'ninetieth_percentile_execution_time',
                         'ninety-ninth_percentile_execution_time', 'slowest_measured_execution_time']
#     or perhaps
        * total_visits
        * total_execution_time
        * average_execution_time
        * visits_per_ip
        * unique_visitors
        * fastest_measured_execution_time
        * fastest_quartile_execution_time
        * median_execution_time
        * slowest_quartile_execution_time
        * ninetieth_percentile_execution_time
        * ninety-ninth_percentile_execution_time
        * slowest_measured_execution_time

    - start_date, end_date: The start- and end dates of the datetime range in which the desired information lies.
        Both start_date and end_date are inclusive resp. upper- and lower bounds of this datetime range.
        If start_date is not provided, it defaults to 1970-1-1.
        If end_date is not provided, it defaults to the current utc time.

        It is assumed both start_date and end_date are provided in utc time.
    - granularity: Since end_date is inclusive, a time granularity is required in order to determine how much time from
        end_date on should be included as well. The possibilities here are: 'year', 'month', 'week', 'day', 'hour' and 'minute'.
        If granularity is not privided, it defaults to 'day'.
    - timeslice: Indicates the data should be returned as a series of points in time, each 'timeslice' long.
                 'timeslice' overrules 'granularity' in terms of granularity.

    If 'timeslice' is absent, a the returned information is a single value. When it is not, a dictionary is returned,
      containing datetime-value pairs, where 'datetime' is formatted to the granularity of 'timeslice'.
      (e.g. 'timeslice=day' will result in datetimes like '2018-05-29', while 'timeslice=minute' will result in
      datetimes like '2018-05-29T15:45')


    Note that if the dashboard has not yet received any endpoint calls, it will simply return {"message": "Dashboard is empty"}
    """
    # Check dashboard_id
    valid_dashboard, result, http_error = pydash_app.dashboard.find_verified_dashboard(dashboard_id)

    if not valid_dashboard:
        return result, http_error

    params = request.args
    first_endpoint_call_time = valid_dashboard.first_endpoint_call_time()
    if not first_endpoint_call_time:
        logger.info(f"Retrieved empty dashboard {valid_dashboard}")
        result = {"message": "Dashboard is empty"}
        return jsonify(result), 200

    statistic = params.get('statistic')
    start_date = params.get('start_date', default=first_endpoint_call_time.strftime('%Y-%m-%dT%H-%M'))
    end_date = params.get('end_date', default=datetime.utcnow().strftime('%Y-%m-%dT%H-%M'))
    timeslice = params.get('timeslice')
    granularity = params.get('granularity', default='day')
    if not statistic:  # Default to returning the generic dashboard_detail.
        if params.get('start_date') or params.get('end_date') or params.get('timeslice') or params.get('granularity'):
            # Apparently there are some arguments that should not be there.
            logger.warning(f"In dashboards: Invalid combination of arguments: statistic is not present,"
                           f" while {[i for i in params.keys()]} are.")
            result = {'message': f'Invalid combination of arguments: statistic is not present,'
                                 f' while {[i for i in params.keys()]} are.'}
            return jsonify(result), 400
        else:
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
            result = handle_statistic_without_timeslice(valid_dashboard, statistic, start_date, end_date, granularity)
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


def handle_statistic_without_timeslice(dashboard, statistic, start_datetime, end_datetime, granularity):
    """
    These datetimes are treated as inclusive boundaries of a datetime range (e.g. [start_datetime, end_datetime]
    :param dashboard:
    :param statistic:
    :param start_datetime:
    :param end_datetime:
    :param granularity:
    :return: The value of a single statistic over the specified datetime range.
    """
    return dashboard.aggregated_data_daterange(start_datetime, end_datetime, granularity)[statistic]


def handle_statistic_per_timeslice(dashboard, statistic, timeslice, start_datetime, end_datetime):
    """These datetimes are treated as inclusive boundaries of a datetime range (e.g. [start_datetime, end_datetime].
    Assumes start_timedate and end_timedate are both timezone aware, with timezone utc.
    :param dashboard:
    :param statistic:
    :param timeslice:
    :param start_datetime:
    :param end_datetime:
    :return: A dictionary consisting of a datetime string (key)(formatted according to the ISO-8601 standard)
             and the corresponding statistic, over the specified datetime range.
    """
    return dashboard.statistic_per_timeslice(statistic, {}, timeslice, start_datetime, end_datetime)


def match_datetime_string_with_formats(datetime_string):
    """Returns a datetime object of this datetime string if the provided string matched with
     one of the allowed formats. Otherwise, returns None and None."""
    datetime_object = None
    for format_name, format in datetime_formats.items():
        try:
            datetime_object = datetime.strptime(datetime_string, format)
        except ValueError:
            continue
    return datetime_object


def check_allowed_timeslices(timeslice):
    return timeslice in allowed_timeslices


def check_allowed_statistics(statistic):
    return statistic in [stat_class.field_name(stat_class) for stat_class in Aggregator.contained_statistics_classes]


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
