import React, {Component} from 'react';
import './overview.css';
import Grid from 'material-ui/Grid';
import DashTile from './DashTile';

class DashTileGrid extends Component {
    constructor(props) {
        super(props);
        this.state = {
            username: props.username,
        };
    }
    
    render() {
        return(
            <Grid container justify="center">
            {/* For each found dashboard for username */}
                <DashTile title='test1' />
                <DashTile title='test2' />
            </Grid>
        );
    }
    
}

export default DashTileGrid;