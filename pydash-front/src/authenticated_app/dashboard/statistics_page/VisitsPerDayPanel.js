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
import TimesliceTabs from './TimesliceTabs';
import DashboardVisitsGraph from './DashboardVisitsGraph';

// Utils:
import {dict_to_xy_arr} from "../../../utils";



class VisitsFetcher extends Component {
    constructor(props) {
        super(props)
        this.state = {
            loading: false,
            timeslice: "hour",
            visits: [],
        }
    }

    componentWillReceiveProps = (newProps) => {
        if(newProps.timeslice !== this.state.timeslice){
            this.setState(prevState => ({...prevState, loading: true, visits: [], timeslice: newProps.timeslice}));
            this.requestVisitsData();
        }
    }

    requestVisitsData = () => {

        // TODO Once back-end has proper API endpoints, use that one instead of the overall one.
        axios({
            method: 'get',
            withCredentials: true,
            url: window.api_path + '/api/dashboards/' + this.props.dashboard_id,
            data: {
                timeslice: this.props.timeslice,
            },
        }).then((response) => {
            this.setState(prevState => {
                return {
                    ...prevState,
                    loading: false,
                    visits: dict_to_xy_arr(response.data.aggregates.visits_per_day),
                }
            });
        }).catch((error) => {
            console.log('error while fetching dashboard information', error);
        });
    }

    render = () => {
        if(this.state.loading){
            return (<em>Loading...</em>);
        }
        return (
            <DashboardVisitsGraph data={this.state.visits} title="Visits per" tooltip_title="No. visits: " height={400} timeslice={this.state.timeslice} />
        )
    }
}

VisitsFetcher.propTypes = {
    timeslice: PropTypes.string.isRequired,
}


class VisitsPerDayPanel extends Component {
    constructor(props) {
        super(props);
        /* this.state = {
         *     visits: [],
         * }; */
    }



    render = () => {
        return (
            <ExpansionPanel>
                <ExpansionPanelSummary expandIcon={<ExpandMoreIcon />}>
                    <h3>No. Visitors</h3>
                </ExpansionPanelSummary>
                <ExpansionPanelDetails>
                    <TimesliceTabs>
                        <VisitsFetcher dashboard_id={this.props.dashboard_id}/>
                    </TimesliceTabs>
                </ExpansionPanelDetails>
            </ExpansionPanel>
        )
    }
}

VisitsPerDayPanel.propTypes = {
    dashboard_id: PropTypes.string.isRequired,
};

export default VisitsPerDayPanel;
