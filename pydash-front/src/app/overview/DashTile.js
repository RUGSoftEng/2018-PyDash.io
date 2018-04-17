import React, {Component} from 'react';

import './overview.css';
import Grid from 'material-ui/Grid';
import Card, { CardContent } from 'material-ui/Card';
import { withStyles } from 'material-ui/styles';

import NavLink from 'react-router-dom/NavLink';
import Button from 'material-ui/Button';

const styles = {
    Card: {
        minWidth: 200,
        minHeight: 100,
        'background-color': '#3f51b5',
    }
};


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

    render() { 
        return(
            <Grid item xs={2} sm={2}>
                <Card>
                    <CardContent>
                        <h2>{this.props.title}</h2>
                        <Button component={NavLink} to={'/dashboard/view/' + this.props.dashboard_id} >View statistics</Button>
                    </CardContent>
                </Card>
            </Grid>
        );
    }
}

export default withStyles(styles)(DashTile);
