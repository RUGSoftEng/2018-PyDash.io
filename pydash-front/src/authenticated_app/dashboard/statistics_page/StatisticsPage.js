import React, { Component } from 'react';
import PropTypes from 'prop-types';

import axios from 'axios';

// Contents:
import VisitsPerDayPanel from './VisitsPerDayPanel';
import UniqueVisitorsPerDayPanel from './UniqueVisitorsPerDayPanel';
import EndpointExecutionTimesPanel from './EndpointExecutionTimesPanel';
import ExecutionTimesTable from './ExecutionTimesTable';

// Helper:
import {dict_to_xy_arr} from "../../../utils";

class StatisticsPage extends Component {
    constructor(props) {
        super(props);
        this.divRef = React.createRef();
        this.state = {
            dashboard: null,
            visits_per_day: [],
            unique_visitors_per_day: [],
            average_execution_times: [],
            error: "",
            width: 0,
        };
    }

    componentDidMount() {
        console.log(this.divRef);
        this.setState(prevState => {
            /* const width =  this.divRef.current.clientWidth;*/
            const width = window.screen.width;
            return {...prevState, width: width}
        })

        axios(window.api_path + '/api/dashboards/' + this.props.dashboard.id, {
            method: 'get',
            withCredentials: true
        }).then((response) => {
            //console.log(response);
            if (response.data.hasOwnProperty('error')) {
                this.setState(prevState => {
                    return {
                        ...prevState,

                        dashboard: response.data,

                        total_visits: response.data.aggregates.total_visits,
                        visits_per_day: dict_to_xy_arr(response.data.aggregates.visits_per_day),
                        unique_visitors_per_day: dict_to_xy_arr(response.data.aggregates.unique_visitors_per_day),
                        error: response.data.error,
                    }
                });
            } else {
                this.setState(prevState => {
                    return {
                        ...prevState,


                        dashboard: response.data,

                        total_visits: response.data.aggregates.total_visits,
                        visits_per_day: dict_to_xy_arr(response.data.aggregates.visits_per_day),
                        unique_visitors_per_day: dict_to_xy_arr(response.data.aggregates.unique_visitors_per_day),
                    };
                });
            }
        }).catch((error) => {
            console.log('error while fetching dashboard information', error);
        });
    }

    render() {
        if(this.props.dashboard === null || this.state.dashboard === null) {
            return (<h2>Loading...</h2>);
        }
        return (

                <div ref={this.divRef} >
                    <h2>Dashboard: {this.state.dashboard.name ? this.state.dashboard.name : this.state.dashboard.url}</h2>
                    <h3>{this.state.error}</h3>
                    <div>
                        <VisitsPerDayPanel dashboard_id={this.props.dashboard.id} />
                        <UniqueVisitorsPerDayPanel dashboard_id={this.props.dashboard.id} />
                        <ExecutionTimesTable dashboard_id={this.props.dashboard.id} />
                        <EndpointExecutionTimesPanel dashboard_id={this.props.dashboard.id} />
                    </div>
                </div>
        );
    }
}

StatisticsPage.propTypes = {
    dashboard: PropTypes.shape({
        id: PropTypes.string.isRequired,
        url: PropTypes.string.isRequired,
    }).isRequired,
};


export default StatisticsPage;
