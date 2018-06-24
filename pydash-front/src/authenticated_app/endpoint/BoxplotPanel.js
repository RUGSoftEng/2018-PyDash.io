import React from 'react';

import ExpansionPanel, { ExpansionPanelSummary, ExpansionPanelDetails } from 'material-ui/ExpansionPanel';
import ExpandMoreIcon from '@material-ui/icons/ExpandMore';

import { Boxplot } from 'react-boxplot';
import ResponsiveGraphWrapper from '../../common/ResponsiveGraphWrapper';

class BoxplotPanel extends React.Component {

    render = () => {
        console.log("BOXPLOTDATA", this.props.data.aggregates);
        if (!this.props.data.aggregates) {
            return(<h2>Loading...</h2>);
        } else {
            return (
                <ExpansionPanel>
                    <ExpansionPanelSummary expandIcon={<ExpandMoreIcon/>}>
                        <h3>Execution times boxplot</h3>
                    </ExpansionPanelSummary>
                    <ExpansionPanelDetails>
                        <ResponsiveGraphWrapper height={200} >
                            <Boxplot
                                width={400}
                                height={40}
                                orientation="horizontal"
                                min={0}
                                max={this.props.data.aggregates.slowest_measured_execution_time + this.props.data.aggregates.fastest_measured_execution_time}
                                stats={ {
                                    whiskerLow: this.props.data.aggregates.fastest_measured_execution_time,
                                    quartile1: this.props.data.aggregates.fastest_quartile_execution_time,
                                    quartile2: this.props.data.aggregates.median_execution_time,
                                    quartile3: this.props.data.aggregates.slowest_quartile_execution_time,
                                    whiskerHigh: this.props.data.aggregates.slowest_measured_execution_time,
                                    outliers: [],
                                }}
                            />
                        </ResponsiveGraphWrapper>
                    </ExpansionPanelDetails>
                </ExpansionPanel>
            );
        }
    }
}

export default BoxplotPanel;