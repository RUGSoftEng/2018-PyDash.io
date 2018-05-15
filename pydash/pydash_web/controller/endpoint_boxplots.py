
from flask import jsonify
from flask_login import current_user
import pydash_app.dashboard
import pydash_logger
import pydash_app.dashboard.services


logger = pydash_logger.Logger(__name__)


def endpoint_boxplots(dashboard_id):
    # Check whether dashboard_id is valid.

    # TODO split the exceptions into key and value errors (see delete_dashboard.py)
    try:
        dashboard = pydash_app.dashboard.find(dashboard_id)
    except Exception:
        result = {'message': f'Dashboard_id {dashboard_id} is invalid.'}
        logger.warning(f'Endpoint_boxplots failure - Dashboard_id {dashboard_id} is invalid. '
                       f'Current user: {current_user}')
        return jsonify(result), 400

    # Check whether user may view dashboard.
    if str(dashboard.user_id) != str(current_user.id):
        result = {'message': f'Current user is not allowed to access dashboard {dashboard_id}'}
        logger.warning(f'Endpoint_boxplots failure - User {current_user} is not allowed to access dashboard {dashboard_id}')
        return jsonify(result), 403

    dashboard = pydash_app.dashboard.find(dashboard_id)
    endpoint_boxplot_list = [_boxplot_data(endpoint) for endpoint in dashboard.endpoints.values()]
    logger.info(f'Endpoint boxplots successful -  data from dashboard {dashboard} requested')
    return jsonify(endpoint_boxplot_list), 200


def _boxplot_data(endpoint):
    aggregated_data = endpoint.aggregated_data()

    return {'endpoint_name':                            endpoint.name,
            'average_execution_time':                   aggregated_data['average_execution_time'],
            'fastest_measured_execution_time':          aggregated_data['fastest_measured_execution_time'],
            'fastest_quartile_execution_time':          aggregated_data['fastest_quartile_execution_time'],
            'median_execution_time':                    aggregated_data['median_execution_time'],
            'slowest_quartile_execution_time':          aggregated_data['slowest_quartile_execution_time'],
            'ninetieth_percentile_execution_time':      aggregated_data['ninetieth_percentile_execution_time'],
            'ninety-ninth_percentile_execution_time':   aggregated_data['ninety-ninth_percentile_execution_time'],
            'slowest_measured_execution_time':          aggregated_data['slowest_measured_execution_time']
            }
