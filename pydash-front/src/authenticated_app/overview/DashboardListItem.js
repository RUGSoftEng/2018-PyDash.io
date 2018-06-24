import React, {Component} from 'react';


// Visual:
import Grid from 'material-ui/Grid';
import Card, { CardContent } from 'material-ui/Card';
import { withStyles } from 'material-ui/styles';
import './overview.css';
import NavLink from 'react-router-dom/NavLink';
import Warning from '@material-ui/icons/Warning';


const styles = {
    Card: {
        minWidth: 200,
        minHeight: 100,
    }
};

/**
 * The `DashboardListItem` displays some general information about the given dashboard;
 *
 * This component is to be used as part of a `DashboardList`.
 */
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
                <NavLink to={'/overview/dashboards/' + this.props.dashboard_id} className="DashboardTileLink">
                    <Card className="DashboardTile">
                        <CardContent>
                            <h2>{this.props.title}{this.props.error ? <Warning color="error"/> : ""}</h2>
                        </CardContent>
                    </Card>
                </NavLink>
            </Grid>
        );
    }
}

export default withStyles(styles)(DashboardListItem);
