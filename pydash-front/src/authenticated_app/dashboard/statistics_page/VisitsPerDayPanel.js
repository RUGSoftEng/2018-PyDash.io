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
import VisitsGraph from './VisitsGraph';

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
    componentDidUpdate = (prevProps, _prevState, snapshot) => {
        if(this.props.timeslice === this.state.timeslice){
            return
        }
        if(this.state.visits[this.props.timeslice] === undefined){
            this.requestVisitsData(this.props);
            this.setState(prevState =>
                ({...prevState, loading: true, timeslice: this.props.timeslice}));
        } else {
            this.setState(prevState => ({...prevState, timeslice: this.props.timeslice}))
        }
    }

    componentDidMount = () => {
        this.requestVisitsData(this.props);
    }

    requestVisitsData = (props) => {
        // TODO Once back-end has proper API endpoints, use that one instead of the overall one.
        axios({
            method: 'get',
            withCredentials: true,
            url: window.api_path + '/api/dashboards/' + props.dashboard_id + '?timeslice=' + props.timeslice,
        }).then((response) => {
            this.setState(prevState => {
                const timeslice_visits = dict_to_xy_arr(response.data.aggregates.unique_visitors_per_day)
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
            <VisitsGraph data={this.state.visits[this.state.timeslice]} title="Visits per" tooltip_title="No. visits: " height={400} timeslice={this.state.timeslice} />
        )
    }
}

VisitsFetcher.propTypes = {
    timeslice: PropTypes.string,
}


function VisitsPerDayPanel(props) {
    return (
        <ExpansionPanel>
            <ExpansionPanelSummary expandIcon={<ExpandMoreIcon />}>
                <h3>No. Visitors</h3>
            </ExpansionPanelSummary>
            <ExpansionPanelDetails>
                <TimesliceTabs>
                    <VisitsFetcher dashboard_id={props.dashboard_id}/>
                </TimesliceTabs>
            </ExpansionPanelDetails>
        </ExpansionPanel>
    )
}

VisitsPerDayPanel.propTypes = {
    dashboard_id: PropTypes.string.isRequired,
};

export default VisitsPerDayPanel;
