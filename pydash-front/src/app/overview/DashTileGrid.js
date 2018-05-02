import React, {Component} from 'react';
import './overview.css';
import Grid from 'material-ui/Grid';
import DashTile from './DashTile';
import { withStyles } from 'material-ui/styles';
import axios from 'axios';
import Card from 'material-ui/Card'
import {CardActions, CardHeader, CardMedia, CardTitle, CardText} from 'material-ui/Card';
import CreateIcon from 'material-ui-icons/Create';
import { NavLink } from 'react-router-dom'
import { ListItem, ListItemIcon, ListItemText } from 'material-ui/List';
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

class DashTileGrid extends Component {
    constructor(props) {
        super(props);
        this.state = {
            dashboards: [],
        };
    }
    
    componentDidMount() {
      axios('http://localhost:5000/api/dashboards', {
        method: 'get',
        withCredentials: true
      }).then((response) => {
        console.log('found some data', response);
        
        
        this.setState(prevState => {
          let newState = prevState;
          newState.dashboards = response.data;
          
          console.log(newState);
          
          return newState;
        });
      }).catch((error) => {
        console.log('error', error);
      });
    }
 
    render() {
        const {classes} = this.props;
        
        let tiles = [];
        let counter = 0;
        
        for (let i in this.state.dashboards) {
          let id = this.state.dashboards[i].id;
          let url = this.state.dashboards[i].url;
          tiles.push(<DashTile key={counter} title={url} dashboard_id={id} xs={12} />);
          counter += 1;
        }

        return(
            <Grid container spacing={24} className={classes.root}>

            <Card>
              {/* <CardActions>
              <ListItem button component={NavLink} to={'/dashboard/settings'}>
                <ListItemIcon>
                    <CreateIcon />
                </ListItemIcon>
            </ListItem>
                </CardActions>
              Hola */}
              </Card>
                {/* For each found dashboard for username */}
                {tiles}
                    
            </Grid>
        );
    }
}

export default withStyles(styles)(DashTileGrid);
