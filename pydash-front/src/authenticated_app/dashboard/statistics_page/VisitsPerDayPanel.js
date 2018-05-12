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
            loading: true,
            timeslice: "hour",
            visits: [],
        }
    }

    componentWillReceiveProps = (newProps) => {
        if(newProps.timeslice !== this.state.timeslice && this.state.visits[newProps.timeslice] === undefined){
            this.setState(prevState =>
                ({...prevState, loading: true, timeslice: newProps.timeslice}));
            this.requestVisitsData();
        }
    }

    componentDidMount = () => {
        this.requestVisitsData();
    }

    requestVisitsData = () => {
        // TODO Once back-end has proper API endpoints, use that one instead of the overall one.
        axios({
            method: 'get',
            withCredentials: true,
            url: window.api_path + '/api/dashboards/' + this.props.dashboard_id + '?timeslice=' + this.props.timeslice,
            data: {
                timeslice: this.props.timeslice,
            },
        }).then((response) => {
            this.setState(prevState => {
                const timeslice_visits = dict_to_xy_arr(response.data.aggregates.visits_per_day)
                let new_visits = prevState.visits
                new_visits[prevState.timeslice] = timeslice_visits;
                return {
                    ...prevState,
                    loading: false,
                    visits: new_visits,
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
            <DashboardVisitsGraph data={this.state.visits[this.state.timeslice]} title="Visits per" tooltip_title="No. visits: " height={400} timeslice={this.state.timeslice} />
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
