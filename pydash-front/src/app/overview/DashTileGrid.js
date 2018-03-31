import React, {Component} from 'react';
import './overview.css';
import Grid from 'material-ui/Grid';
import DashTile from './DashTile';
import { withStyles } from 'material-ui/styles';
import axios from 'axios';
import Typography from 'material-ui/Typography';

/* import '../../../node_modules/react-vis/dist/style.css';*/
/* import {XYPlot, VerticalBarSeries, VerticalGridLines, HorizontalGridLines, XAxis, YAxis} from 'react-vis';*/

import { Line } from '@nivo/line'


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

const data = [{
    id: "foobar",
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

            this.setState(prevState =>{
                let newState = prevState;
                newState.total_visits = "" + mock_data.aggregates.total_visits;
                newState.visits_per_day = dict_to_xy_arr(mock_data.aggregates.visits_per_day)
                console.log(newState)

                return newState;
            })

        });
    }
    
    render() {
        const {classes, theme} = this.props;


        const data2 = [{
            id: 'asdf',
            data: [
                {x: 1, y: 2},
                {x: 2, y: 1},
                {x: 3, y: 3}
            ]
        }]

        const data3 = [
  {
    "id": "whisky",
    "color": "hsl(270, 70%, 50%)",
    "data": [
      {
        "color": "hsl(53, 70%, 50%)",
        "x": "DZ",
        "y": 44
      },
      {
        "color": "hsl(226, 70%, 50%)",
        "x": "BJ",
        "y": 16
      },
      {
        "color": "hsl(148, 70%, 50%)",
        "x": "BB",
        "y": 45
      },
      {
        "color": "hsl(296, 70%, 50%)",
        "x": "VN",
        "y": 20
      },
      {
        "color": "hsl(219, 70%, 50%)",
        "x": "GG",
        "y": 0
      },
      {
        "color": "hsl(334, 70%, 50%)",
        "x": "TZ",
        "y": 11
      },
      {
        "color": "hsl(190, 70%, 50%)",
        "x": "LK",
        "y": 31
      },
      {
        "color": "hsl(19, 70%, 50%)",
        "x": "CL",
        "y": 1
      },
      {
        "color": "hsl(319, 70%, 50%)",
        "x": "TR",
        "y": 50
      }
    ]
  },
  {
    "id": "rhum",
    "color": "hsl(299, 70%, 50%)",
    "data": [
      {
        "color": "hsl(344, 70%, 50%)",
        "x": "DZ",
        "y": 12
      },
      {
        "color": "hsl(21, 70%, 50%)",
        "x": "BJ",
        "y": 16
      },
      {
        "color": "hsl(328, 70%, 50%)",
        "x": "BB",
        "y": 11
      },
      {
        "color": "hsl(298, 70%, 50%)",
        "x": "VN",
        "y": 22
      },
      {
        "color": "hsl(277, 70%, 50%)",
        "x": "GG",
        "y": 2
      },
      {
        "color": "hsl(307, 70%, 50%)",
        "x": "TZ",
        "y": 1
      },
      {
        "color": "hsl(326, 70%, 50%)",
        "x": "LK",
        "y": 50
      },
      {
        "color": "hsl(332, 70%, 50%)",
        "x": "CL",
        "y": 40
      },
      {
        "color": "hsl(125, 70%, 50%)",
        "x": "TR",
        "y": 17
      }
    ]
  },
  {
    "id": "gin",
    "color": "hsl(319, 70%, 50%)",
    "data": [
      {
        "color": "hsl(53, 70%, 50%)",
        "x": "DZ",
        "y": 58
      },
      {
        "color": "hsl(251, 70%, 50%)",
        "x": "BJ",
        "y": 20
      },
      {
        "color": "hsl(80, 70%, 50%)",
        "x": "BB",
        "y": 19
      },
      {
        "color": "hsl(256, 70%, 50%)",
        "x": "VN",
        "y": 8
      },
      {
        "color": "hsl(304, 70%, 50%)",
        "x": "GG",
        "y": 27
      },
      {
        "color": "hsl(295, 70%, 50%)",
        "x": "TZ",
        "y": 37
      },
      {
        "color": "hsl(11, 70%, 50%)",
        "x": "LK",
        "y": 4
      },
      {
        "color": "hsl(349, 70%, 50%)",
        "x": "CL",
        "y": 37
      },
      {
        "color": "hsl(298, 70%, 50%)",
        "x": "TR",
        "y": 46
      }
    ]
  },
  {
    "id": "vodka",
    "color": "hsl(80, 70%, 50%)",
    "data": [
      {
        "color": "hsl(103, 70%, 50%)",
        "x": "DZ",
        "y": 18
      },
      {
        "color": "hsl(247, 70%, 50%)",
        "x": "BJ",
        "y": 46
      },
      {
        "color": "hsl(79, 70%, 50%)",
        "x": "BB",
        "y": 11
      },
      {
        "color": "hsl(320, 70%, 50%)",
        "x": "VN",
        "y": 58
      },
      {
        "color": "hsl(155, 70%, 50%)",
        "x": "GG",
        "y": 8
      },
      {
        "color": "hsl(78, 70%, 50%)",
        "x": "TZ",
        "y": 30
      },
      {
        "color": "hsl(226, 70%, 50%)",
        "x": "LK",
        "y": 50
      },
      {
        "color": "hsl(41, 70%, 50%)",
        "x": "CL",
        "y": 34
      },
      {
        "color": "hsl(233, 70%, 50%)",
        "x": "TR",
        "y": 24
      }
    ]
  },
  {
    "id": "cognac",
    "color": "hsl(331, 70%, 50%)",
    "data": [
      {
        "color": "hsl(4, 70%, 50%)",
        "x": "DZ",
        "y": 58
      },
      {
        "color": "hsl(274, 70%, 50%)",
        "x": "BJ",
        "y": 22
      },
      {
        "color": "hsl(146, 70%, 50%)",
        "x": "BB",
        "y": 8
      },
      {
        "color": "hsl(208, 70%, 50%)",
        "x": "VN",
        "y": 6
      },
      {
        "color": "hsl(116, 70%, 50%)",
        "x": "GG",
        "y": 19
      },
      {
        "color": "hsl(224, 70%, 50%)",
        "x": "TZ",
        "y": 56
      },
      {
        "color": "hsl(22, 70%, 50%)",
        "x": "LK",
        "y": 23
      },
      {
        "color": "hsl(124, 70%, 50%)",
        "x": "CL",
        "y": 50
      },
      {
        "color": "hsl(196, 70%, 50%)",
        "x": "TR",
        "y": 28
      }
    ]
  }
]

        console.log('visits_per_day', this.state.visits_per_day)
        
        return(
            <div className={classes.root}>
            <h2>Dashboard Information</h2>

                <Line
                    data={[{id:'No. of pageviews per day:', data: this.state.visits_per_day}]}
                    width={500}
                    height={500}
                    curve="monotoneX"
                    axisBottom={{
                        "orient": "bottom",
                        "tickSize": 5,
                        "tickPadding": 5,
                        "tickRotation": 45,
                        "legend": "date",
                        "legendOffset": 36,
                        "legendPosition": "center"
                    }}
                    axisLeft={{
                        "orient": "left",
                        "tickSize": 5,
                        "tickPadding": 5,
                        "tickRotation": 0,
                        "legend": "No. pageviews",
                        "legendOffset": -40,
                        "legendPosition": "center"
                    }}
                    margin={{
                        "top": 50,
                        "right": 100,
                        "bottom": 150,
                        "left": 100
                    }}
                    colors={["aquamarine", "blue", "cyan"]}
                    dotSize={10}
                    dotColor="inherit:darker(0.5)"
                    dotBorderWidth={2}
                    dotBorderColor="#ffffff"
                    enableDotLabel={true}
                    dotLabel="y"
                    dotLabelYOffset={-12}
                    animate={true}
                    enableArea={true}
                />
                <Grid container justify="center">
                {/* For each found dashboard for username */}
                    <DashTile title='lorem ipsum dolor sid amet, onzin en nog wat meer padding die ik ter plekke uit mijn duim zuig' xs='6'/>
                    <DashTile title='test2' xs='6'/>
                    <DashTile title='eenveeltelangwoorddatnietbestaat' xs='12' />
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
