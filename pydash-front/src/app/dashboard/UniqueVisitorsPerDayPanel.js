import React, { Component } from 'react';
import axios from 'axios';

import DashboardVisitsGraph from './DashboardVisitsGraph';

import ExpansionPanel, {
    ExpansionPanelSummary,
    ExpansionPanelDetails,
} from 'material-ui/ExpansionPanel';
import ExpandMoreIcon from '@material-ui/icons/ExpandMore';

import {dict_to_xy_arr} from "../../utils";

class UniqueVisitorsPerDayPanel extends Component {
    constructor(props) {
        super(props);
        this.state = {
            unique_visitors_per_day: [],
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
                    unique_visitors_per_day: dict_to_xy_arr(response.data.aggregates.unique_visitors_per_day),
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
                    <h3>Unique Visitors Per Day</h3>
                </ExpansionPanelSummary>
                <ExpansionPanelDetails>
                    <DashboardVisitsGraph data={this.state.unique_visitors_per_day} title="Unique visitors per day:" tooltip_title="No. visits: "/>
                </ExpansionPanelDetails>
            </ExpansionPanel>
        )
    }
}

export default UniqueVisitorsPerDayPanel;
