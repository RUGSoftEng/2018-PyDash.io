import React, {Component} from 'react';
import PropTypes from 'prop-types';

// Contents:
import { Line } from '@nivo/line'

// Utils:
import ResponsiveGraphWrapper from '../../../common/ResponsiveGraphWrapper';

class DashboardVisitsGraph extends Component {
    render() {
        let width = this.props.width;
        if(width < 0 || width === undefined){
            width = 1;
        }
        return (
            <ResponsiveGraphWrapper height={this.props.height} >
            <h4>{this.props.title} {this.props.timeslice}</h4>
            <Line
            data={[{id: this.props.tooltip_title, data: this.props.data}]}
            height={this.props.height}
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
                "bottom": 130,
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
            </ResponsiveGraphWrapper>
        );
    }
}

DashboardVisitsGraph.propTypes = {
    data: PropTypes.array.isRequired,
    title: PropTypes.string.isRequired,
    tooltip_title: PropTypes.string.isRequired,
    height: PropTypes.number.isRequired,
    timeslice: PropTypes.string.isRequired
};

export default DashboardVisitsGraph;
