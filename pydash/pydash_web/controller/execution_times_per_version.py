"""
Handles requests for tdigest data of response times per version.
"""

from flask import jsonify

import pydash_app.dashboard.repository
import pydash_logger
from .utils import execution_times

logger = pydash_logger.Logger(__name__)


def execution_times_per_version(dashboard_id, endpoint_name=None):
    valid_dashboard, result, http_error = pydash_app.dashboard.find_verified_dashboard(dashboard_id)

    if not valid_dashboard:
        return result, http_error

    if not endpoint_name:
        aggregator_group_containter = valid_dashboard
    else:
        valid_endpoint = valid_dashboard.endpoints.get(endpoint_name)
        if not valid_endpoint:
            logger.warning(f'In execution_times_per_version: Endpoint name {endpoint_name} is invalid.')
            result = {'message': f'Endpoint name {endpoint_name} is invalid.'}
            return jsonify(result), 400
        aggregator_group_containter = valid_endpoint

    values_per_version = _execution_times_per_version(aggregator_group_containter)

    logger.info('Successfully retrieved execution time per version.')
    return jsonify(values_per_version), 200


def _execution_times_per_version(aggregator_group_container):
    return_dict = {}
    versions = aggregator_group_container.statistic('versions', {})
    for version in versions:
        return_dict[version] = execution_times(aggregator_group_container, filters={'version': version})

    return return_dict
