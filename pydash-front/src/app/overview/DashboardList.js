import React, {Component} from 'react';
import './overview.css';
import Grid from 'material-ui/Grid';
import DashboardListItem from './DashboardListItem';
import { withStyles } from 'material-ui/styles';
import axios from 'axios';

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

class DashboardList extends Component {
    constructor(props) {
        super(props);
        this.state = {
            dashboards: [],
            error: "",
        };
    }

    componentDidMount() {
        console.log("Before DashboardList endpoint call")
      axios(window.api_path + '/api/dashboards', {
        method: 'get',
        withCredentials: true
      }).then((response) => {
        console.log('found some data', response);
        if (response.data.hasOwnProperty('error')) {
          console.log("Error found");
          this.setState(prevState => {
            return {
              ...prevState,
              dashboards: response.data,
              error: response.data.error,
            };
          });
        } else { 
          this.setState(prevState => {
            return {
              ...prevState,

              dashboards: response.data,
            };
          });
        }
      }).catch((error) => {
        console.log('error while fetching dashboards information', error);
      });
    }

    render() {
        const {classes} = this.props;

        const tiles = this.state.dashboards.map((dashboard, index) => {
            return <DashboardListItem key={index} title={dashboard.url} dashboard_id={dashboard.id} error={dashboard.error} />
        })

        return(
            <Grid container spacing={24} className={classes.root}>
                {/* For each found dashboard for username */}
                {tiles.length > 0 ? tiles : <h4><em style={{color: "grey"}}>No Dashboards have been added to your account yet.</em></h4>}
            </Grid>
        );
    }
}

export default withStyles(styles)(DashboardList);