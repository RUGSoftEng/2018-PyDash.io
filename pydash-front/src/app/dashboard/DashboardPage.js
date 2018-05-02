import React, { Component } from 'react';
import { Breadcrumb } from 'react-breadcrumbs';
import axios from 'axios';

import VisitsPerDayPanel from './VisitsPerDayPanel';
import UniqueVisitorsPerDayPanel from './UniqueVisitorsPerDayPanel';
import {dict_to_xy_arr} from "../../utils";
import EndpointExecutionTimesPanel from './EndpointExecutionTimesPanel';
import ExecutionTimesTable from './ExecutionTimesTable';

// Transforms a hashmap of key-value pairs into an array of {x: key, y: value} objects.
// TODO move to a helper JS file.
/*function dict_to_xy_arr(dict){
   let res =  Object.entries(dict).map(function([key, value]){
   return {x: key, y: value}
   });
   console.log('dict_to_xy_array', res);
   return res;
   }*/

/*const styles = theme => ({
   root: {
   flexGrow: 1,
   },
   paper: {
   padding: theme.spacing.unit * 2,
   textAlign: 'center',
   color: theme.palette.text.secondary,
   },
   });*/



class Board extends Component {
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

        axios(window.api_path + '/api/dashboards/' + this.props.id, {
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
        if(this.state.dashboard === null) {
            return (<h2>Loading...</h2>);
        }
        return (

                <div ref={this.divRef} >
                    <h2>Dashboard: {this.state.dashboard.url}</h2>
                    <h3>{this.state.error}</h3>
                    <div>
                        <VisitsPerDayPanel dashboard_id={this.props.id} />
                        <UniqueVisitorsPerDayPanel dashboard_id={this.props.id} />
                        <ExecutionTimesTable dashboard_id={this.props.id} />
                        <EndpointExecutionTimesPanel dashboard_id={this.props.id} />
                    </div>
                </div>
        );
    }
}

export default Board;
