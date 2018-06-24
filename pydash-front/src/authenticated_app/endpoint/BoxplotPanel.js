import React from 'react';

import ExpansionPanel, { ExpansionPanelSummary, ExpansionPanelDetails } from 'material-ui/ExpansionPanel';
import ExpandMoreIcon from '@material-ui/icons/ExpandMore';

import { Boxplot } from 'react-boxplot';
import ResponsiveGraphWrapper from '../../common/ResponsiveGraphWrapper';

class BoxplotPanel extends React.Component {

    render = () => {
        console.log("BOXPLOTDATA", this.props.data);
        return (
            <ExpansionPanel>
                <ExpansionPanelSummary expandIcon={<ExpandMoreIcon/>}>
                    <h3>Execution times boxplot</h3>
                </ExpansionPanelSummary>
                <ExpansionPanelDetails>
                    <ResponsiveGraphWrapper height={150} >
                        <Boxplot
                            width={400}
                            height={40}
                            orientation="horizontal"
                            min={0}
                            max={this.props.data.slowest_measured_execution_time + this.props.data.fastest_measured_execution_time}
                            stats={ {
                                whiskerLow: this.props.data.fastest_measured_execution_time,
                                quartile1: this.props.data.fastest_quartile_execution_time,
                                quartile2: this.props.data.median_execution_time,
                                quartile3: this.props.data.slowest_quartile_execution_time,
                                whiskerHigh: this.props.data.slowest_measured_execution_time,
                                outliers: [],
                            }}
                        />
                        <br />
                        <div className="BoxplotTable" style={{maxWidth: "600px", margin: "0 auto"}}>
                            <table width="100%">
                                <thead>
                                <tr>
                                    <th>Fastest</th>
                                    <th>First quartile</th>
                                    <th>Median</th>
                                    <th>Last quartile</th>
                                    <th>Slowest</th>
                                </tr>
                                </thead>
                                <tbody>
                                <tr>
                                    <th>{this.props.data.slowest_measured_execution_time} ms</th>
                                    <th>{this.props.data.fastest_quartile_execution_time} ms</th>
                                    <th>{this.props.data.median_execution_time} ms</th>
                                    <th>{this.props.data.slowest_quartile_execution_time} ms</th>
                                    <th>{this.props.data.slowest_measured_execution_time} ms</th>
                                </tr>
                                </tbody>
                            </table>
                        </div>
                    </ResponsiveGraphWrapper>
                </ExpansionPanelDetails>
            </ExpansionPanel>
        );
    }
}

export default BoxplotPanel;