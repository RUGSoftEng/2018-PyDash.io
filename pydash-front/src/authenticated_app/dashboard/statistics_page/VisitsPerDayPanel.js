import React, { Component } from 'react';
import PropTypes from 'prop-types';

import axios from 'axios';

// Visual:
import ExpansionPanel, {
    ExpansionPanelSummary,
    ExpansionPanelDetails,
} from 'material-ui/ExpansionPanel';
import ExpandMoreIcon from '@material-ui/icons/ExpandMore';

// Contents:
import DashboardVisitsGraph from './DashboardVisitsGraph';

// Utils:
import {dict_to_xy_arr} from "../../../utils";


class VisitsPerDayPanel extends Component {
    constructor(props) {
        super(props);
        this.state = {
            visits_per_day: [],
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
                    visits_per_day: dict_to_xy_arr(response.data.aggregates.visits_per_day),
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
                    <h3>Visits Per Day</h3>
                </ExpansionPanelSummary>
                <ExpansionPanelDetails>
                    <DashboardVisitsGraph data={this.state.visits_per_day} title="Visits per day:" tooltip_title="No. visits: "/>
                </ExpansionPanelDetails>
            </ExpansionPanel>
        )
    }
}

VisitsPerDayPanel.propTypes = {
    dashboard_id: PropTypes.string.isRequired,
};

export default VisitsPerDayPanel;
