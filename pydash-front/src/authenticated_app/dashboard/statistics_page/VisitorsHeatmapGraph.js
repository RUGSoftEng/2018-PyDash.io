import React, {Component} from 'react';
import PropTypes from 'prop-types';

// Contents:
import { HeatMapCanvas } from '@nivo/heatmap';

// Utils:
import ResponsiveGraphWrapper from '../../../common/ResponsiveGraphWrapper';

function getKeys() {
    const keys = [];
    for (let i = 0; i < 24; i++) {
        if (i < 10) {
            keys[i] = "0" + i + ":00";
        } else {
            keys[i] = "" + i + ":00";
        }
    }
    return keys;
}

/**
 * Heatmap of visitors that have been visiting this Dashboard.
 */
class VisitorsHeatmapGraph extends Component {
    render() {
        let keys = getKeys();
        console.log("Keys: ", keys);
        return (
            <ResponsiveGraphWrapper height={this.props.height}>
                <h4>{this.props.title}</h4>
                <HeatMapCanvas
                    height={this.props.height}
                    data={this.props.data}
                    keys={keys}
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
                        "legend": "Date",
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
