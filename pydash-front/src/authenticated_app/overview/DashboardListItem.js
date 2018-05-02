import React, {Component} from 'react';


// Visual:
import Grid from 'material-ui/Grid';
import Card, { CardContent } from 'material-ui/Card';
import { withStyles } from 'material-ui/styles';
import './overview.css';
import NavLink from 'react-router-dom/NavLink';


const styles = {
    Card: {
        minWidth: 200,
        minHeight: 100,
    }
};

class DashboardListItem extends Component {
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
            <Grid item xs={12} sm={12}>
                <NavLink to={'/dashboard/view/' + this.props.dashboard_id} className="DashboardTileLink">
                <Card className="DashboardTile">
                    <CardContent>
                        <h2>{this.props.title}</h2>
                        <h3>{this.props.error}</h3>
                    </CardContent>
                </Card>
                </NavLink>
            </Grid>
        );
    }
}

export default withStyles(styles)(DashboardListItem);
