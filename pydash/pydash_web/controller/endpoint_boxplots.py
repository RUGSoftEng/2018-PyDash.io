
from flask import jsonify
import pydash_app.dashboard
import pydash_logger


logger = pydash_logger.Logger(__name__)


def endpoint_boxplots(dashboard_id):
    dashboard = pydash_app.dashboard.find(dashboard_id)
    endpoint_boxplot_list = [_boxplot_data(endpoint) for endpoint in dashboard.endpoints.values()]
    logger.info(f'Endpoint boxplots from dashboard {dashboard} requested')
    return jsonify(endpoint_boxplot_list), 200


def _boxplot_data(endpoint):
    aggregated_data = endpoint.aggregated_data()

    return {'endpoint_name':                            endpoint.name,
            'average_execution_time':                   aggregated_data['average_execution_time'],
            'fastest_measured_execution_time':          aggregated_data['fastest_measured_execution_time'],
            'fastest_quartile_execution_time':          aggregated_data['fastest_quartile_execution_time'],
            'slowest_quartile_execution_time':          aggregated_data['slowest_quartile_execution_time'],
            'ninetieth_percentile_execution_time':      aggregated_data['ninetieth_percentile_execution_time'],
            'ninety-ninth_percentile_execution_time':   aggregated_data['ninety-ninth_percentile_execution_time'],
            'slowest_measured_execution_time':          aggregated_data['slowest_measured_execution_time']
            }
