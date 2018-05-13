import React, { Component } from 'react';
import PropTypes from 'prop-types';


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
import {requestStatisticData} from "./statistics_utils"


class StatisticFetcher extends Component {
    statistic_name = null
    constructor(props) {
        super(props)
        this.state = {
            loading: true,
            timeslice: "hour",
            statistic_data: [],
        }
    }
    componentDidUpdate = (prevProps, _prevState, snapshot) => {
        if(this.props.timeslice === this.state.timeslice){
            return
        }
        if(this.state.statistic_data[this.props.timeslice] === undefined){
            this.requestVisitsData();
            this.setState(prevState =>
                ({...prevState, loading: true, timeslice: this.props.timeslice}));
        } else {
            this.setState(prevState => ({...prevState, timeslice: this.props.timeslice}))
        }
    }

    componentDidMount = () => {
        this.requestVisitsData();
    }

    requestVisitsData = async () => {
        const timeslice_statistic_data = await requestStatisticData(this.props.dashboard_id, this.statistic_name, this.props.timeslice);

        // TODO Once back-end has proper API endpoints, use that one instead of the overall one.
        this.setState(prevState => {
            let statistic_data = prevState.statistic_data;
            statistic_data[prevState.timeslice] = timeslice_statistic_data;
            return {
                ...prevState,
                loading: false,
                statistic_data: statistic_data,
            }
        });
    }

    render = () => {
        if(this.state.loading){
            return (<em>Loading...</em>);
        }
        return (
            "Do not use this component directly! Rather, use a child-class of it."
        )
    }
}

StatisticFetcher.propTypes = {
    timeslice: PropTypes.string,
}


export default StatisticFetcher;
