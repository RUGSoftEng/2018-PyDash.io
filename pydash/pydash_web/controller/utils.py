"""
The go-to place for general methods that can be used in multiple controller methods.
"""


def execution_times(aggregator_group_container, filters={}):
    aggregated_data = aggregator_group_container.aggregated_data(filters)

    return {'average_execution_time':                   aggregated_data['average_execution_time'],
            'fastest_measured_execution_time':          aggregated_data['fastest_measured_execution_time'],
            'fastest_quartile_execution_time':          aggregated_data['fastest_quartile_execution_time'],
            'median_execution_time':                    aggregated_data['median_execution_time'],
            'slowest_quartile_execution_time':          aggregated_data['slowest_quartile_execution_time'],
            'ninetieth_percentile_execution_time':      aggregated_data['ninetieth_percentile_execution_time'],
            'ninety-ninth_percentile_execution_time':   aggregated_data['ninety-ninth_percentile_execution_time'],
            'slowest_measured_execution_time':          aggregated_data['slowest_measured_execution_time']
            }
