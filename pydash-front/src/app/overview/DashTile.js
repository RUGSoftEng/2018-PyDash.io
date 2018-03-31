import React, {Component} from 'react';
import axios from 'axios';

import './overview.css';
import Grid from 'material-ui/Grid';
import GridList, {GridListTile} from 'material-ui/GridList';
import Card, { CardContent } from 'material-ui/Card';
import { withStyles } from 'material-ui/styles';
import Typography from 'material-ui/Typography';

import DashboardVisitsGraph from './DashboardVisitsGraph'

const styles = {
    card: {
        minWidth: 100,
        minHeight: 100,
        'background-color': '#3f51b5',
    }
};

// Transforms a hashmap of key-value pairs into an array of {x: key, y: value} objects.
// TODO move to a helper JS file.
function dict_to_xy_arr(dict){
    let res =  Object.entries(dict).map(function([key, value]){
        return {x: key, y: value}
    });
    console.log('dict_to_xy_array', res);
    return res;
}


class DashTile extends Component {
    constructor(props) {
        super(props);
        this.state = {
            col: props.xs,
            total_visits: "?",
            visits_per_day: [],
            unique_visitors_per_day: [],
        };
    }

    componentDidMount() {
        console.log("TEST")
        // TODO: Get dashboard_id from newProps
        const dashboard_id = this.props.dashboard_id
        axios('http://localhost:5000/api/dashboards/' + dashboard_id, {
            method: 'get',
            withCredentials: true
        }).then((response) => {
            console.log('success', response);
            this.setState(prevState =>{
                let newState = prevState;
                newState.total_visits = "" + response.data.aggregates.total_visits;
                newState.visits_per_day = dict_to_xy_arr(response.data.aggregates.visits_per_day)
                newState.unique_visitors_per_day = dict_to_xy_arr(response.data.aggregates.unique_visitors_per_day)
                console.log(newState)

                return newState;
            })
        }).catch((error) => {
            console.log('error', error);

            /* this.setState(prevState =>{
                *     let newState = prevState;
                *     newState.total_visits = "" + mock_data.aggregates.total_visits;
                *     newState.visits_per_day = dict_to_xy_arr(mock_data.aggregates.visits_per_day)
                *     console.log(newState)

                *     return newState;
                * })
            */
        });
    }


    render() { 
        return(
            <Grid item xs={12}>
                <Card>
                    <CardContent>
                        <h2>{this.props.title}</h2>
                        <h3>Total Visits: {this.state.total_visits}</h3>
                        <GridList cellHeight='auto'>
                            <GridListTile>
                                <DashboardVisitsGraph data={this.state.visits_per_day} title="Visits Per Day" tooltip_title="No. visits: "/>
                            </GridListTile>
                            <GridListTile>
                                <DashboardVisitsGraph data={this.state.unique_visitors_per_day} title="Unique Visitors Per Day" tooltip_title="No. unique visits: "/>
                            </GridListTile>
                        </GridList>
                    </CardContent>
                </Card>
            </Grid>
        );
    }
}

export default withStyles(styles)(DashTile);
