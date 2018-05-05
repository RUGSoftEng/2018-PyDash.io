import React, { Component } from 'react';

// Button stuff
import Add from '@material-ui/icons/Add'

// Contents:
import DashboardList from './DashboardList';
import { Button } from 'material-ui';


class OverviewPage extends Component {
    render() {
        return (

            <div>
                <h2>Dashboards</h2>
                <Button classname="NewDashboardButton" variant="raised" color="primary">
                    Add dashboard
                    <Add />
                </Button>
                <DashboardList dashboards={this.props.dashboards} />
            </div>
        );
    }
}

export default OverviewPage;
