import React, {Component} from 'react';
import './overview.css';
import Grid from 'material-ui/Grid';
import DashTile from './DashTile';
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


class DashTileGrid extends Component {  
    constructor(props) {
        super(props);
        this.state = {
            username: props.username,
        };
    }

    componentDidMount() {
        axios('http://localhost:5000/api/dashboards/123', {
            method: 'get',
            withCredentials: true
        }).then((response) => {
            console.log('success', response);
        }).catch((error) => {
            console.log('error', error);
        });

    }
    
    render() {
        const {classes, theme} = this.props;
        
        return(
            <div className={classes.root}>
                <Grid container justify="center">
                {/* For each found dashboard for username */}
                    <DashTile title='lorem ipsum dolor sid amet, onzin en nog wat meer padding die ik ter plekke uit mijn duim zuig' xs='6'/>
                    <DashTile title='test2' xs='6'/>
                    <DashTile title='eenveeltelangwoorddatnietbestaat' xs='12' />
                </Grid>
            </div>
        );
    }
    
}

export default withStyles(styles)(DashTileGrid);
