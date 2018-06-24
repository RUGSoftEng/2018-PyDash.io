import React, { Component } from 'react';
import PropTypes from 'prop-types';

import axios from 'axios';

// Visual:
import ExpandMoreIcon from '@material-ui/icons/ExpandMore';

// Contents:
import ExecutionTimesGraph from './ExecutionTimesGraph';
import ExpansionPanel, {
    ExpansionPanelSummary,
    ExpansionPanelDetails,
} from 'material-ui/ExpansionPanel';


// Utils:
import { api_to_bar_data} from "../../../utils";

/**
 * Panel containing the `EndpointExecutionTimesGraph`.
 */
class EndpointExecutionTimesPanel extends Component {
    constructor(props) {
        super(props);
        this.state = {
            average_execution_times: [],
        };
    }

    componentDidMount() {
        axios(window.api_path + '/api/dashboards/' + this.props.dashboard_id, {
            method: 'get',
            withCredentials: true
        }).then((response) => {
            console.log("Returned data", response);
            this.setState(prevState => {
                return {
                    ...prevState,
                    average_execution_times: api_to_bar_data(response.data.endpoints),
                }
            });
        }).catch((error) => {
            console.log('error while fetching dashboard information', error);
        });
    }

    render = () => {

        return (
            <ExpansionPanel>
                <ExpansionPanelSummary expandIcon={<ExpandMoreIcon />}>
                    <h3>Average execution time per endpoint</h3>
                </ExpansionPanelSummary>
                <ExpansionPanelDetails>
                    <ExecutionTimesGraph data={this.state.average_execution_times} height={this.state.average_execution_times.length*80} title="Average execution time per endpoint" />
                </ExpansionPanelDetails>
            </ExpansionPanel>
        )
    }
}

EndpointExecutionTimesPanel.propTypes = {
    dashboard_id: PropTypes.string.isRequired,
};

export default EndpointExecutionTimesPanel;
