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
import WidthAwareContainer from "../../../common/WidthAwareContainer";
import ContainerDimensions from 'react-container-dimensions';


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
    '5': {
        'aggregates': {
            'average_execution_time': 2
        },
        'name': "overview4"
    },
    '6': {
        'aggregates': {
            'average_execution_time': 23
        },
        'name': "index2"
    },
    '7': {
        'aggregates': {
            'average_execution_time': 48
        },
        'name': "user2"
    },
    '8': {
        'aggregates': {
            'average_execution_time': 10
        },
        'name': "dashboard2"
    },
    '9': {
        'aggregates': {
            'average_execution_time': 25
        },
        'name': "testpage2"
    },
    '10': {
        'aggregates': {
            'average_execution_time': 2
        },
        'name': "overview2"
    }, 
    '11': {
        'aggregates': {
            'average_execution_time': 2
        },
        'name': "overview3"
    },

};

class WidthShower extends Component {
    render = () => (
        <strong>Width: {this.props.width}</strong>
    );
}

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
                    <h3>Average execution time per endpoint</h3>
                </ExpansionPanelSummary>
                <ExpansionPanelDetails>
                    {/* <ExecutionTimesGraph data={this.state.average_execution_times} height={this.state.average_execution_times.length*80} title="Average execution time per endpoint" /> */}
                    <ContainerDimensions>
                        <WidthShower />
                    </ContainerDimensions>
                </ExpansionPanelDetails>
            </ExpansionPanel>
        )
    }
}

EndpointExecutionTimesPanel.propTypes = {
    dashboard_id: PropTypes.string.isRequired,
};

export default EndpointExecutionTimesPanel;
