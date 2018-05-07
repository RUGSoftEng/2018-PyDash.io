import React, { Component } from 'react';

// Button stuff
import Add from '@material-ui/icons/Add';

// Form stuff
import AddDashboardDialog from './AddDashboardDialog';

// Contents:
import DashboardList from './DashboardList';
import { Button } from 'material-ui';


class OverviewPage extends Component {
    state = {
        open: false,
    }

    handleClickOpen = () => {
        this.setState({open: true});
    };

    handleClose = () => {
        this.setState({open: false});
    };

    render() {
        return (

            <div>
                <h2>Dashboards</h2>
                <Button onClick={this.handleClickOpen} classname="NewDashboardButton" variant="raised" color="primary">
                    Add dashboard
                    <Add />
                </Button>
                <AddDashboardDialog 
                    open={this.state.open}
                    onClose={this.handleClose}
                />
                <DashboardList dashboards={this.props.dashboards} />
            </div>
        );
    }
}

export default OverviewPage;