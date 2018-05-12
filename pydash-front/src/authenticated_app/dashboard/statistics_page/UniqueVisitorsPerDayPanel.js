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

class UniqueVisitsFetcher extends Component {
    constructor(props) {
        super(props)
        this.state = {
            loading: true,
            timeslice: "day",
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
        if(this.state.loading) {
            return (<em>Loading...</em>);
        }
        return (
            <DashboardVisitsGraph data={this.state.visits[this.state.timeslice]} title="Unique visitors per" tooltip_title="No. unique visits: " height={400} timeslice={this.state.timeslice} />
        )
    }
}

UniqueVisitsFetcher.propTypes = {
    timeslice: PropTypes.string,
}

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
                    <TimesliceTabs>
                        <UniqueVisitsFetcher dashboard_id={this.props.dashboard_id}/>
                    </TimesliceTabs>
                </ExpansionPanelDetails>
            </ExpansionPanel>
        )
    }
}

UniqueVisitorsPerDayPanel.propTypes = {
    dashboard_id: PropTypes.string.isRequired,
};

export default UniqueVisitorsPerDayPanel;
