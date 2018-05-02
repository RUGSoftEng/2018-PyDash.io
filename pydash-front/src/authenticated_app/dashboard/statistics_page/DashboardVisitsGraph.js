import React, {Component} from 'react';
import PropTypes from 'prop-types';

// Contents:
import { ResponsiveLine } from '@nivo/line'


class DashboardVisitsGraph extends Component {
    render() {
        return (<div style={{width: "100%"}}>
            <h4>{this.props.title}</h4>
            <ResponsiveLine
                data={[{id: this.props.tooltip_title, data: this.props.data}]}
                height={this.props.height ? this.props.height : 300}
                curve="monotoneX"
                axisBottom={{
                    "orient": "bottom",
                    "tickSize": 5,
                    "tickPadding": 5,
                    "tickRotation": 45,
                    "legend": "date",
                    "legendOffset": 36,
                    "legendPosition": "center"
                }}
                axisLeft={{
                    "orient": "left",
                    "tickSize": 5,
                    "tickPadding": 5,
                    "tickRotation": 0,
                    "legend": "No. pageviews",
                    "legendOffset": -40,
                    "legendPosition": "center"
                }}
                margin={{
                    "top": 50,
                    "right": 50,
                    "bottom": 50,
                    "left": 50
                }}
                colors={["aquamarine", "blue", "cyan"]}
                dotSize={10}
                dotColor="inherit:darker(0.5)"
                dotBorderWidth={2}
                dotBorderColor="#ffffff"
                enableDotLabel={true}
                dotLabel="y"
                dotLabelYOffset={-12}
                animate={true}
                enableArea={true}
            />
            </div>
        );
    }
}

DashboardVisitsGraph.propTypes = {
    data: PropTypes.array.isRequired,
    title: PropTypes.string.isRequired,
    tooltip_title: PropTypes.string.isRequired,
};

export default DashboardVisitsGraph;
