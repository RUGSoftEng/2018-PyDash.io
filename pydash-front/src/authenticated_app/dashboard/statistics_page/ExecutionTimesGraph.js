import React, {Component} from 'react';
import PropTypes from 'prop-types';

// Contents:
import { Bar } from '@nivo/bar';

// Utils:
import ResponsiveGraphWrapper from '../../../common/ResponsiveGraphWrapper';

class ExecutionTimesGraph extends Component {
    render() {
        return (
            <ResponsiveGraphWrapper height={this.props.height}>
                <h4>{this.props.title}</h4>
                <Bar
                    height={this.props.height}
                    data={this.props.data}
                    keys={[
                        "average_execution_time",
                    ]}
                    indexBy="name"
                    margin={{
                        "top": 50,
                        "right": 50,
                        "bottom": 100,
                        "left": 100
                    }}
                    padding={0.3}
                    layout="horizontal"
                    colors="nivo"
                    colorBy="id"
                    borderColor="inherit:darker(1.6)"
                    axisBottom={{
                        "orient": "bottom",
                        "tickSize": 5,
                        "tickPadding": 15,
                        "tickRotation": 0,
                    }}
                    axisLeft={{
                        "orient": "left",
                        "tickSize": 5,
                        "tickPadding": 5,
                        "tickRotation": 0,
                    }}
                    labelSkipWidth={12}
                    labelSkipHeight={12}
                    labelTextColor="inherit:darker(1.6)"
                    animate={true}
                    motionStiffness={90}
                    motionDamping={15}
                />
            </ResponsiveGraphWrapper>
        );
    }
}

ExecutionTimesGraph.propTypes = {
    data: PropTypes.array.isRequired,
    title: PropTypes.string.isRequired,
};

export default ExecutionTimesGraph;
