import React, { Component } from 'react';

// Contents:
import DashboardList from './DashboardList';


class OverviewPage extends Component {
    render() {
        return (

            <div>
                <h2>Dashboards</h2>
                <DashboardList dashboards={this.props.dashboards} />
            </div>
        );
    }
}

export default OverviewPage;
