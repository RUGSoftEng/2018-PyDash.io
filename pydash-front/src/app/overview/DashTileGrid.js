import React, {Component} from 'react';
import './overview.css';
import Grid from 'material-ui/Grid';
import DashTile from './DashTile';
import { withStyles } from 'material-ui/styles';
import axios from 'axios';
import Typography from 'material-ui/Typography';

import '../../../node_modules/react-vis/dist/style.css';
import {XYPlot, VerticalBarSeries, VerticalGridLines, HorizontalGridLines, XAxis, YAxis} from 'react-vis';

import { ResponsiveLine } from '@nivo/line'


const styles = theme => ({
  root: {
    flexGrow: 1,
  },
  paper: {
    padding: theme.spacing.unit * 2,
    textAlign: 'center',
    color: theme.palette.text.secondary,
  },
});

const mock_data = {
    "aggregates": {
        "average_execution_time": 0.24285714285714285,
        "total_execution_time": 1.7,
        "total_visits": 7,
        "unique_visitors": 2,
        "unique_visitors_per_day": {
            "2018-03-25": 1,
            "2018-03-27": 1,
            "2018-03-28": 1,
            "2018-03-29": 1,
            "2018-03-30": 2
        },
        "visits_per_day": {
            "2018-03-25": 1,
            "2018-03-27": 1,
            "2018-03-28": 1,
            "2018-03-29": 1,
            "2018-03-30": 3
        },
        "visits_per_ip": {
            "127.0.0.1": 5,
            "127.0.0.2": 2
        }
    },
    "endpoints": [
        {
            "aggregates": {
                "average_execution_time": 0.3,
                "total_execution_time": 0.6,
                "total_visits": 2,
                "unique_visitors": 2,
                "unique_visitors_per_day": {
                    "2018-03-30": 2
                },
                "visits_per_day": {
                    "2018-03-30": 2
                },
                "visits_per_ip": {
                    "127.0.0.1": 1,
                    "127.0.0.2": 1
                }
            },
            "enabled": true,
            "name": "foo"
        },
        {
            "aggregates": {
                "average_execution_time": 0.22000000000000003,
                "total_execution_time": 1.1,
                "total_visits": 5,
                "unique_visitors": 2,
                "unique_visitors_per_day": {
                    "2018-03-25": 1,
                    "2018-03-27": 1,
                    "2018-03-28": 1,
                    "2018-03-29": 1,
                    "2018-03-30": 1
                },
                "visits_per_day": {
                    "2018-03-25": 1,
                    "2018-03-27": 1,
                    "2018-03-28": 1,
                    "2018-03-29": 1,
                    "2018-03-30": 1
                },
                "visits_per_ip": {
                    "127.0.0.1": 4,
                    "127.0.0.2": 1
                }
            },
            "enabled": true,
            "name": "bar"
        }
    ],
    "id": "35944bb3-e5d7-42f3-b1c6-a26232b4367a",
    "url": "http://foo.io"
}

// Transforms a hashmap of key-value pairs into an array of {x: key, y: value} objects.
function dict_to_xy_arr(dict){
    let res =  Object.entries(dict).map(function([key, value]){
        return {x: key, y: value}
    });
    console.log('dict_to_xy_array', res);
    return res;
}

function destringify_date_keys(dict){
    let res =  Object.entries(dict).map(function([key, value]){
        let obj = {}
        obj[new Date(key)] = value;
        return obj;
    })
    .reduce((acc, kv) => Object.assign(acc, kv), {})
    console.log('destringify_date_keys', res);
    return res;
}


class DashTileGrid extends Component {
    constructor(props) {
        super(props);
        this.state = {
            username: props.username,
            total_visits: "?",
            visits_per_day: [],
        };
    }

    componentDidMount() {
        axios('http://localhost:5000/api/dashboards/123', {
            method: 'get',
            withCredentials: true
        }).then((response) => {
            console.log('success', response);
            this.setState(prevState =>{
                let newState = prevState;
                newState.total_visits = "" + response.data.aggregates.total_visits;
                newState.visits_per_day = dict_to_xy_arr(destringify_date_keys(response.data.aggregates.visits_per_day))
                console.log(newState)

                return newState;
            })
        }).catch((error) => {
            console.log('error', error);
        });
    }
    
    render() {
        const {classes, theme} = this.props;

        const data = [{
            id: "foo",
            data: [
                {
                    x: "2018-03-25",
                    y: 1
                },
                {
                    x: "2018-03-27",
                    y: 1
                },
                {
                    x: "2018-03-28",
                    y: 1
                },
                {
                    x: "2018-03-29",
                    y: 1
                },
                {
                    x: "2018-03-30",
                    y: 3
                }
            ]}]

        const data2 = [
            {x: 1, y: 2},
            {x: 2, y: 1},
            {x: 3, y: 3}]
        
        return(
            <div className={classes.root}>
                <Grid container justify="center">
                {/* For each found dashboard for username */}
                    <DashTile title='lorem ipsum dolor sid amet, onzin en nog wat meer padding die ik ter plekke uit mijn duim zuig' xs='6'/>
                    <DashTile title='test2' xs='6'/>
                    <DashTile title='eenveeltelangwoorddatnietbestaat' xs='12' />
                    <ResponsiveLine data={data2} />
                    <Typography>Total Visits: {this.state.total_visits}</Typography>
            {/* <XYPlot height={300} width={300}>
                <VerticalBarSeries data={data2} />
                </XYPlot> */}
                </Grid>
            </div>
        );
    }
    
}

export default withStyles(styles)(DashTileGrid);
