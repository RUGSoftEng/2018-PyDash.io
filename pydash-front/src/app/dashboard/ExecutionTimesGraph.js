import React, {Component} from 'react';
import { ResponsiveBar } from '@nivo/bar';

class ExecutionTimesGraph extends Component {
    render() {
        return (<div style={{width: "100%"}}>
        <h4>{this.props.title}</h4>
        <ResponsiveBar
            data={this.props.data}
            keys={[
                "average_execution_time",
            ]}
            indexBy="name"
            margin={{
                "top": 50,
                "right": 130,
                "bottom": 50,
                "left": 60
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
                "legend": "Endpoint",
                "legendPosition": "center",
                "legendOffset": 36
            }}
            axisLeft={{
                "orient": "left",
                "tickSize": 5,
                "tickPadding": 5,
                "tickRotation": 0,
                "legend": "Time",
                "legendPosition": "center",
                "legendOffset": -40
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
                    "itemWidth": 100,
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

export default ExecutionTimesGraph;