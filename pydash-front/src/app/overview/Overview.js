import React, { Component } from 'react';
import DashboardList from './DashboardList';

import { Breadcrumb } from 'react-breadcrumbs'

class Overview extends Component {
    render() {
        return (

            <div>
                <h2>Dashboards</h2>
                <DashboardList dashboards={this.props.dashboards} />
            </div>
        );
    }
}

export default Overview;
