import React, {Component} from 'react';
import PropTypes from 'prop-types';

// Contents:
import { HeatMap } from '@nivo/heatmap';

// Utils:
import ResponsiveGraphWrapper from '../../../common/ResponsiveGraphWrapper';

class VisitorsHeatmapGraph extends Component {
    render() {
        return (
            <ResponsiveGraphWrapper height={this.props.height}>
                <h4>{this.props.title}</h4>
                <HeatMap
                    height={this.props.height}
                    data={this.props.data}
                    keys={[
                        "00:00",
                        "01:00",
                        "02:00",
                        "03:00",
                        "04:00",
                        "05:00",
                        "06:00",
                        "07:00",
                        "08:00",
                        "09:00",
                        "10:00",
                        "11:00",
                        "12:00",
                        "13:00",
                        "14:00",
                        "15:00",
                        "16:00",
                        "17:00",
                        "18:00",
                        "19:00",
                        "20:00",
                        "21:00",
                        "22:00",
                        "23:00",
                    ]}
                    indexBy="date"
                    margin={{
                        "top": 100,
                        "right": 60,
                        "bottom": 60,
                        "left": 60
                    }}
                    colors="YlOrRd"
                    forceSquare={true}
                    axisTop={{
                        "orient": "top",
                        "tickSize": 5,
                        "tickPadding": 5,
                        "tickRotation": -90,
                        "legend": "",
                        "legendOffset": 36
                    }}
                    axisLeft={{
                        "orient": "left",
                        "tickSize": 5,
                        "tickPadding": 5,
                        "tickRotation": 0,
                        "legend": "country",
                        "legendPosition": "center",
                        "legendOffset": -100
                    }}
                    cellOpacity={1}
                    cellBorderColor="inherit:darker(0.4)"
                    labelTextColor="inherit:darker(1.8)"
                    defs={[
                        {
                            "id": "lines",
                            "type": "patternLines",
                            "background": "inherit",
                            "color": "rgba(0, 0, 0, 0.1)",
                            "rotation": -45,
                            "lineWidth": 4,
                            "spacing": 7
                        }
                    ]}
                    fill={[
                        {
                            "id": "lines"
                        }
                    ]}
                    animate={true}
                    motionStiffness={80}
                    motionDamping={9}
                    hoverTarget="cell"
                    cellHoverOthersOpacity={0.25}
                />
            </ResponsiveGraphWrapper>
        );
    }
}

VisitorsHeatmapGraph.propTypes = {
    data: PropTypes.array.isRequired,
    title: PropTypes.string.isRequired,
};

export default VisitorsHeatmapGraph;
