
from flask import jsonify
import pydash_app.dashboard
import pydash_logger
import pydash_app.dashboard.services
from .utils import execution_times


logger = pydash_logger.Logger(__name__)


def endpoint_execution_times_boxplots(dashboard_id, endpoint_name=None):
    valid_dashboard, result, http_error = pydash_app.dashboard.find_verified_dashboard(dashboard_id)

    if not valid_dashboard:
        return result, http_error

    if not endpoint_name:
        return_value = {
            endpoint.name: execution_times(endpoint)
            for endpoint in valid_dashboard.endpoints.values()
        }
    else:
        valid_endpoint = valid_dashboard.endpoints.get(endpoint_name)
        if not valid_endpoint:
            logger.warning(f'In endpoint_execution_times_boxplots: Endpoint name {endpoint_name} is invalid.')
            result = {'message': f'Endpoint name {endpoint_name} is invalid.'}
            return jsonify(result), 400

        return_value = execution_times(valid_endpoint)

    logger.info(f'Endpoint boxplots successful -  data from dashboard {valid_dashboard} requested')
    return jsonify(return_value), 200
