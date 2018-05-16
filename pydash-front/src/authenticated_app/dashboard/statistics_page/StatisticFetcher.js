import React, { Component } from 'react';
import PropTypes from 'prop-types';

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
        requestStatisticData(this.props.dashboard_id, this.statistic_name, this.props.timeslice, timeslice_statistic_data => {
            // TODO Once back-end has proper API endpoints, use that one instead of the overall one.
            console.log("TIMESLICE DATA:", this.statistic_name, timeslice_statistic_data)
            this.setState(prevState => {
                let statistic_data = prevState.statistic_data;
                statistic_data[this.props.timeslice] = timeslice_statistic_data;
                console.log("NEW STATISTIC DATA", statistic_data, this.props.timeslice, timeslice_statistic_data);
                return {
                    ...prevState,
                    loading: false,
                    statistic_data: statistic_data,
                }
            });
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
