import React, {Component} from 'react';
import { Line } from '@nivo/line'

class DashboardVisitsGraph extends Component {
    constructor(props) {
        super(props);
    }

    render() {
        return (<div>
            <h4>{this.props.title}:</h4>
            <Line
                data={[{id: this.props.tooltip_title, data: this.props.data}]}
                width={500}
                height={400}
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
                    "right": 100,
                    "bottom": 150,
                    "left": 100
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

export default DashboardVisitsGraph;
