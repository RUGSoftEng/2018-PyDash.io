import React, { Component } from 'react';
import axios from 'axios';

//import DashboardVisitsGraph from './DashboardVisitsGraph';
import ExecutionTimesGraph from './ExecutionTimesGraph';

import ExpansionPanel, {
    ExpansionPanelSummary,
    ExpansionPanelDetails,
} from 'material-ui/ExpansionPanel';
import ExpandMoreIcon from '@material-ui/icons/ExpandMore';

import {dict_to_xy_arr, api_to_bar_data} from "../../utils";

// Dummy data for testing average endpoint execution time visualisation.
const endpoints = {
    '0': {
        'aggregates': {
            'average_execution_time': 23
        },
        'name': "index"
    },
    '1': {
        'aggregates': {
            'average_execution_time': 48
        },
        'name': "user"
    },
    '2': {
        'aggregates': {
            'average_execution_time': 10
        },
        'name': "dashboard"
    },
    '3': {
        'aggregates': {
            'average_execution_time': 25
        },
        'name': "testpage"
    },
    '4': {
        'aggregates': {
            'average_execution_time': 2
        },
        'name': "overview"
    },

};

class EndpointExecutionTimesPanel extends Component {
    constructor(props) {
        super(props);
        this.state = {
            average_execution_times: [],
        };
    }
    

    componentDidMount() {
        // TODO Once back-end has proper API endpoints, use that one instead of the overall one.
        axios(window.api_path + '/api/dashboards/' + this.props.dashboard_id, {
            method: 'get',
            withCredentials: true
        }).then((response) => {
            this.setState(prevState => {
                return {
                    ...prevState,
                    average_execution_times: api_to_bar_data(endpoints),
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
                    <h3>Average execution time per endpint</h3>
                </ExpansionPanelSummary>
                <ExpansionPanelDetails>
                    <ExecutionTimesGraph data={this.state.average_execution_times} title="Average execution time per endpoint" tooltip_title="Execution time: "/>
                </ExpansionPanelDetails>
            </ExpansionPanel>
        )
    }
}

export default EndpointExecutionTimesPanel;
