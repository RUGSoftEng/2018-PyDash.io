"""
Manages the lookup and returning of dashboard information of the logged in user, as well as specific .
"""

from flask import jsonify, request

from functools import reduce
from datetime import datetime
from pydash_app.dashboard.aggregator.aggregator_group import static_timeslices, dynamic_timeslices, datetime_formats
from pydash_app.dashboard.aggregator import Aggregator


import pydash_app.dashboard
import pydash_logger

logger = pydash_logger.Logger(__name__)


def dashboard(dashboard_id):
    """
    Lists information of a single dashboard.
    :param dashboard_id: ID of the dashboard to retrieve information from.
    :return: The returned value consists of a tuple of dashboard information, together with a http status code.

    If no arguments are given, a representation of the dashboard itself is returned.
    This route supports the following request arguments:
    - statistic: The name of the statistic of which aggregated information should be returned.
      The currently supported statistics are:
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
        start_date and end_date are the resp. inclusive lower- and exclusive upper bounds of this datetime range.
        If start_date is not provided, it defaults to timestamp of the dashboard's first endpoint call.
        If end_date is not provided, it defaults to the current utc time.
        It is assumed both start_date and end_date are provided in utc time, as well as that they conform to
        the ISO-8601 date and time standard.

    - timeslice: Indicates the data should be returned as a series of points in time, each 'timeslice' long.
        The currently supported timeslices are: 'year', 'month', 'week', 'day', 'hour' and 'minute'.

    - timeslice_is_static: Indicates whether the timeslice should be 'static' (i.e. have a set place in the overarching timespan
        [e.g. W23, or the month of June]) or 'dynamic' (i.e. its start and end can be anything, but its length is set in stone)
        Note that `timeslice_is_static` is mandatory when `timeslice` is provided.

    If 'timeslice' is absent, a the returned information is a single value. When it is not, a dictionary is returned,
      containing datetime-value pairs, where 'datetime' is formatted to the granularity of 'timeslice'.
      (e.g. 'timeslice=day' will result in datetimes like '2018-05-29', while 'timeslice=minute' will result in
      datetimes like '2018-05-29T15:45')


    Note that if the dashboard has not yet received any endpoint calls, it will simply return an empty dictionary.
    """
    # Check dashboard_id
    valid_dashboard, result, http_error = pydash_app.dashboard.find_verified_dashboard(dashboard_id)

    if not valid_dashboard:
        return result, http_error

    params = request.args
    first_endpoint_call_time = valid_dashboard.first_endpoint_call_time()
    if not first_endpoint_call_time:
        logger.info(f"Retrieved empty dashboard {valid_dashboard}")
        result = {}
        return jsonify(result), 200

    statistic = params.get('statistic')
    start_date = params.get('start_date')
    start_date_in_params = not params.get('start_date') is None
    if not start_date_in_params:
        start_date = first_endpoint_call_time.strftime('%Y-%m-%dT%H-%M')

    end_date = params.get('end_date')
    end_date_in_params = not params.get('end_date') is None
    if not end_date_in_params:
        end_date = datetime.utcnow().strftime('%Y-%m-%dT%H-%M')

    timeslice = params.get('timeslice')
    timeslice_is_static = params.get('timeslice_is_static')

    if statistic is None:  # Default to returning the generic dashboard_detail.
        # Check if any other parameter is passed. This would make the request invalid.
        if not reduce(lambda x, y: x and y, map(lambda x: x is None, params.values()), True):
            logger.warning(f"In dashboards: Invalid combination of arguments: statistic is not present,"
                           f" while {[i for i in params.keys() if i]} are.")
            result = {'message': f'Invalid combination of arguments: statistic is not present,'
                                 f' while {[i for i in params.keys() if i]} are.'}
            return jsonify(result), 400
        else:
            logger.info(f"Retrieved dashboard {valid_dashboard}")
            return jsonify(_dashboard_detail(valid_dashboard)), 200
    else:
        # Check formatting of start- and end dates.
        start_date_format_is_valid, start_date_format = match_datetime_string_with_formats(start_date)
        if not start_date_format_is_valid:
            logger.warning('In dashboard: Invalid format of start_date.')
            result = {"message": "Invalid format of start_date."}
            return jsonify(result), 400

        end_date_format_is_valid, end_date_format = match_datetime_string_with_formats(end_date)
        if not end_date_format_is_valid:
            logger.warning('In dashboard: Invalid format of end_date.')
            result = {"message": "Invalid format of end_date."}
            jsonify(result), 400

        start_date_time_value = datetime.strptime(start_date, start_date_format)
        end_date_time_value = datetime.strptime(end_date, end_date_format)

        # Check for valid start_date-end_date pair.
        if start_date_time_value >= end_date_time_value:  # >= since end_date is the exclusive upper bound now.
            logger.warning('In dashboard: ValueError: start_date must be smaller than end_date.')
            result = {"message": "ValueError: start_date must be smaller than end_date."}
            jsonify(result), 400

        # Check whether the provided statistic is valid.
        if not check_allowed_statistics(statistic):
            logger.warning(f'In dashboard: Statistic {statistic} is not supported for use.')
            result = {'message': f'Statistic {statistic} is not supported for use.'}
            return jsonify(result), 400

        if not timeslice:  # We are dealing with statistics that only deal with single aggregates, not multiple.
            result = handle_statistic_without_timeslice(valid_dashboard, statistic, start_date_time_value,
                                                        end_date_time_value)
        else:
            # Check whether timeslice_is_static is passed as an argument (as it is mandatory at this point)
            if timeslice_is_static is None:
                logger.warning(f'In dashboard: Argument \'timeslice_is_static\' not provided, while timeslice {timeslice} is.')
                result = {'message': 'Argument \'timeslice_is_static\' should be provided when \'timeslice\' is provided.'}
                return jsonify(result), 400

            try:
                timeslice_is_static = string_to_bool(timeslice_is_static)
            except ValueError:
                logger.warning(f'In dashboard: Argument \'timeslice_is_static\' has an invalid value: {timeslice_is_static}.')
                result = {'message': f'Argument \'timeslice_is_static\' has an invalid value: {timeslice_is_static}.'
                                     f' It should be either "True" or "False"'}
                return jsonify(result), 400

            if not check_allowed_timeslices(timeslice, timeslice_is_static):
                if timeslice_is_static:
                    message = 'Static'
                else:
                    message = 'Dynamic'
                message += f' timeslice {timeslice} is not supported.'
                logger.warning(f'In dashboard: ' + message)
                result = {'message': message}
                return jsonify(result), 400

            # Handle timeslice statistics
            result = handle_statistic_per_timeslice(valid_dashboard, statistic, timeslice, timeslice_is_static,
                                                    start_date_time_value, end_date_time_value,
                                                    start_date_in_params, end_date_in_params)

        logger.info(f'Successfully handled dashboard-statistic call.'
                    f' statistic={statistic}, timeslice={timeslice}, timeslice_is_static={timeslice_is_static},'
                    f' start_date={start_date}, end_date={end_date}')
        return jsonify(result), 200


def handle_statistic_without_timeslice(dashboard, statistic, start_datetime, end_datetime,
                                       start_date_in_params, end_date_in_params):
    """
    These datetimes are treated as resp. inclusive and exclusive boundaries of a datetime range. (i.e. [start_datetime, end_datetime))
    :param dashboard: A Dashboard instance corresponding to the dashboard of which the value of a statistic is desired.
    :param statistic: A string denoting what statistic to handle.
    :param start_datetime: A datetime object denoting the inclusive lower bound of the desired datetime range.
    :param end_datetime: A datetime object denoting the exclusive upper bound of the desired datetime range.
    :param start_date_in_params: A boolean indicating whether the start_date was in the request parameters.
    :param end_date_in_params: A boolean indicating whether the end_date was in the request parameters.
    :return: The value of a single statistic over the specified datetime range.
    """
    if not start_date_in_params and not end_date_in_params:
        # This is significantly faster than trying to combine aggregators,
        #  as there exists a single aggregator that aggregates over all endpoint calls.
        return dashboard.statistic(statistic)
    else:
        return dashboard.aggregated_data_daterange(start_date=start_datetime,
                                                   end_date=end_datetime
                                                   )[statistic]


def handle_statistic_per_timeslice(dashboard, statistic, timeslice, timeslice_is_static, start_datetime, end_datetime,
                                   start_date_in_params, end_date_in_params):
    """These datetimes are treated as inclusive boundaries of a datetime range (e.g. [start_datetime, end_datetime].
    Assumes start_timedate and end_timedate are both timezone aware, with timezone utc.
    :param dashboard: The Dashboard object to retrieve the time-sliced statistic information from.
    :param statistic: A string denoting the statistic in question. The complete amount of allowed statistics is:
      - 'total_visits'
      - 'total_execution_time'
      - 'average_execution_time'
      - 'visits_per_ip'
      - 'unique_visitors'
      - 'fastest_measured_execution_time'
      - 'fastest_quartile_execution_time'
      - 'median_execution_time'
      - 'slowest_quartile_execution_time'
      - 'ninetieth_percentile_execution_time'
      - 'ninety-ninth_percentile_execution_time'
      - 'slowest_measured_execution_time'
      - 'versions'
    :param timeslice: A string denoting the granularity of the timeslice (e.g. 'day' to slice up the time range in entire days.)
    :param timeslice_is_static: A boolean indicating whether the timeslice should be interpreted as being either 'static' or 'dynamic'.
    :param start_datetime: A datetime instance denoting the inclusive lower bound of the desired datetime range.
    :param end_datetime: A datetime instance denoting the exclusive upper bound of the desired datetime range.
    :param start_date_in_params: A boolean indicating whether the start_date was in the request parameters.
    :param end_date_in_params: A boolean indicating whether the end_date was in the request parameters.
    :return: A dictionary consisting of a datetime string (key)(formatted according to the ISO-8601 standard)
             and the corresponding statistic, over the specified datetime range.
    """
    if not start_date_in_params and timeslice_is_static:
        # Truncate start_datetime in order to encompass the whole timeslice.
        from pydash_app.dashboard.aggregator.aggregator_group import truncate_datetime_by_granularity
        start_datetime = truncate_datetime_by_granularity(start_datetime, timeslice)

    if not end_date_in_params and timeslice_is_static:
        # If end_datetime is not at the start of a timeslice, set it to the start of the next timeslice,
        # such that it encompasses the entire timeslice.
        from pydash_app.dashboard.aggregator.aggregator_group import truncate_datetime_by_granularity, convert_unit_to_timedelta
        if end_datetime != truncate_datetime_by_granularity(end_datetime, timeslice):
            end_datetime = truncate_datetime_by_granularity(end_datetime, timeslice)
            end_datetime += convert_unit_to_timedelta(end_datetime, timeslice)

    statistic_dict = dashboard.statistic_per_timeslice(statistic=statistic, timeslice=timeslice,
                                                       timeslice_is_static=timeslice_is_static,
                                                       start_datetime=start_datetime,
                                                       end_datetime=end_datetime,
                                                       )
    return_dict = {}
    # Transform datetime keys into their respective string forms.
    for datetime_value, statistic_value in statistic_dict.items():
        datetime_rendered_string = datetime_to_rendered_string(datetime_value, timeslice, timeslice_is_static)
        return_dict[datetime_rendered_string] = statistic_value

    return return_dict


def string_to_bool(string):
    if string == 'True':
        return True
    elif string == 'False':
        return False
    else:
        raise ValueError("string must be either 'True' or 'False'")


def match_datetime_string_with_formats(datetime_string):
    """
    Matches a datetime string with the allowed datetime formats.
    :param datetime_string: A string denoting a datetime.
    :return: A tuple containing a boolean value and a string denoting a datetime format.
     The boolean value corresponds with whether this datetime string's format is one of the allowed formats.
     The datetime format string corresponds with the format of the provided datetime string. If it doesn't match any of
     the allowed formats, None is returned instead.
    """
    for format_name, format in datetime_formats.items():
        try:
            if datetime.strptime(datetime_string, format):
                return True, format
        except ValueError:
            continue
    return False, None


def datetime_to_rendered_string(datetime_value, granularity, granularity_is_static):
    """
    Returns the to be rendered string representation of the given datetime instance.
    :param datetime_value: The datetime instance to render the string representation of.
    :param granularity: A string denoting the granularity of the `datetime_value`.
    :param granularity_is_static: A boolean denoting whether `granularity` should be interpreted as being 'static' or 'dynamic'.
    :return: Returns a string representing the given `datetime_value` with respects to the given `granularity`.
    """
    if not granularity_is_static and granularity not in dynamic_timeslices:
        return ValueError(f"{granularity} cannot be dynamic.")

    if not granularity_is_static:
        datetime_format = datetime_formats['minute']
    else:
        datetime_format = datetime_formats[granularity]

    return datetime_value.strftime(datetime_format)


def check_allowed_timeslices(timeslice, timeslice_is_static):
    if timeslice_is_static:
        return timeslice in static_timeslices
    else:
        return timeslice in dynamic_timeslices


def check_allowed_statistics(statistic):
    return statistic in [stat_class.field_name(stat_class) for stat_class in Aggregator.contained_statistics_classes]


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
