import React, { Component } from 'react';

// Button stuff
import Add from '@material-ui/icons/Add';

// Form stuff
import AddDashboardDialog from './AddDashboardDialog';

// Contents:
import DashboardList from './DashboardList';
import { Button } from 'material-ui';

/**
 * The `OverviewPage` is the main page the user sees after logging in.
 */
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
                <Button onClick={this.handleClickOpen} className="NewDashboardButton" variant="raised" color="primary">
                    Add dashboard
                    <Add />
                </Button>
                <h2>Dashboards</h2>
                <AddDashboardDialog
                    open={this.state.open}
                    onClose={this.handleClose}
                    callBack={this.props.updateData}
                />

                {((this.props.dashboards == null) ?
                    <h4>
                        <em>
                            Loading...
                        </em>
                    </h4>
                :
                  <DashboardList dashboards={this.props.dashboards} />
                )}
            </div>
        );
    }
}

export default OverviewPage;
