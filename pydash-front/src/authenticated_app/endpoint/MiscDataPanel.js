import React, { Component } from 'react';

import ExpansionPanel, { ExpansionPanelSummary, ExpansionPanelDetails } from 'material-ui/ExpansionPanel';
import ExpandMoreIcon from '@material-ui/icons/ExpandMore';
import ResponsiveGraphWrapper from '../../common/ResponsiveGraphWrapper';

class MiscDataPanel extends Component {
    render = () => {
        return (
            <ExpansionPanel>
                <ExpansionPanelSummary expandIcon={<ExpandMoreIcon/>}>
                    <h3>Other data</h3>
                </ExpansionPanelSummary>
                <ExpansionPanelDetails>
                    <ResponsiveGraphWrapper height={150}>
                        <div className="MiscDataTable" style={{maxWidth: "600px", margin: "0 auto"}}>
                            <table width="100%">
                                <thead>
                                <tr>
                                    <th>Total visits</th>
                                    <th>Unique visitors</th>
                                    <th>Average execution time</th>
                                    <th>Total execution time</th>
                                </tr>
                                </thead>
                                <tbody>
                                <tr>
                                    <th>{this.props.data.total_visits}</th>
                                    <th>{this.props.data.unique_visitors}</th>
                                    <th>{this.props.data.average_execution_time}</th>
                                    <th>{this.props.data.total_execution_time}</th>
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

export default MiscDataPanel;