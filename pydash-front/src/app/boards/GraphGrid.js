import React, {Component} from 'react';
import Grid from 'material-ui/Grid';
import { withStyles } from 'material-ui/styles';
import axios from 'axios';
import DashboardVisitsGraph from './DashboardVisitsGraph';
import Card from 'material-ui/Card';

// Transforms a hashmap of key-value pairs into an array of {x: key, y: value} objects.
// TODO move to a helper JS file.
function dict_to_xy_arr(dict){
  let res =  Object.entries(dict).map(function([key, value]){
      return {x: key, y: value}
  });
  console.log('dict_to_xy_array', res);
  return res;
}

// Transforms the returned endpoint data from the api into a form that can be
// displayed in a nivo bar graph.
function api_to_bar_data(endpoints) {
  let res = [];
  for (let i in endpoints) {
    let name = endpoints[i].name;
    let average_execution_time = endpoints[i].aggregates.average_execution_time;
    res.push({'name': name, 'average_execution_time': average_execution_time});
  }
  console.log('bar data', res);
  return res;
}

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

// Dummy data for testing average endpoint execution time visualisation.
const endpoints = {
  '0': {
    'aggregates': {
      'average_execution_time': 23
    },
    'name': "index"
  },
  '1': {
    'aggregates': {
      'average_execution_time': 48
    },
    'name': "user"
  },
  '2': {
    'aggregates': {
      'average_execution_time': 10
    },
    'name': "dashboard"
  },
  '3': {
    'aggregates': {
      'average_execution_time': 25
    },
    'name': "testpage"
  },
  '4': {
    'aggregates': {
      'average_execution_time': 2
    },
    'name': "overview"
  },

};



class GraphGrid extends Component {
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
    const dashboard_id = this.props.id
    axios(window.api_path + '/api/dashboards/' + dashboard_id, {
        method: 'get',
        withCredentials: true
    }).then((response) => {
        console.log('success', response);
        this.setState(prevState =>{
            let newState = prevState;
            newState.total_visits = "" + response.data.aggregates.total_visits;
            newState.visits_per_day = dict_to_xy_arr(response.data.aggregates.visits_per_day)
            newState.unique_visitors_per_day = dict_to_xy_arr(response.data.aggregates.unique_visitors_per_day)
            newState.average_execution_times = api_to_bar_data(endpoints);
            console.log(newState);

            return newState;
        })
    }).catch((error) => {
        console.log('error', error);
    });
  }

  render() {
    const {classes} = this.props;
    return(
      <Grid container spacing={24} className={classes.root}>
        <Grid item xs={6}>
          <Card>
            <DashboardVisitsGraph data={this.state.visits_per_day} title="Visits per day:" tooltip_title="No. visits: "/>
          </Card>
        </Grid>
        <Grid item xs={6}>
          <Card>
            <DashboardVisitsGraph data={this.state.unique_visitors_per_day} title="Unique visitors per day" tooltip_title="No. unique visits: "/>
          </Card>
        </Grid>
      </Grid>
    );
  }

    
}

export default withStyles(styles)(GraphGrid);
