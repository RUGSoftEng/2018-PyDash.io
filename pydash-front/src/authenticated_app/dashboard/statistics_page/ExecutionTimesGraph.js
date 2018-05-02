import React, {Component} from 'react';
import PropTypes from 'prop-types';

// Contents:
import { Bar } from '@nivo/bar';

class ExecutionTimesGraph extends Component {
    render() {
        return (<div style={{width: "100%"}}>
        <h4>{this.props.title}</h4>
        <Bar
            width={1000}
            height={this.props.height}
            data={this.props.data}
            keys={[
                "average_execution_time",
            ]}
            indexBy="name"
            margin={{
                "top": 50,
                "right": 200,
                "bottom": 50,
                "left": 120
            }}
            padding={0.3}
            layout="horizontal"
            colors="nivo"
            colorBy="id"
            borderColor="inherit:darker(1.6)"
            axisBottom={{
                "orient": "bottom",
                "tickSize": 5,
                "tickPadding": 5,
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
            legends={[
                {
                    "dataFrom": "keys",
                    "anchor": "bottom-right",
                    "direction": "column",
                    "translateX": 120,
                    "itemWidth": 150,
                    "itemHeight": 20,
                    "itemsSpacing": 2,
                    "symbolSize": 20
                }
            ]}
        />
        </div>
        );
    }
}

ExecutionTimesGraph.propTypes = {
    data: PropTypes.array.isRequired,
    title: PropTypes.string.isRequired,
};

export default ExecutionTimesGraph;
