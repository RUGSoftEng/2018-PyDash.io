import React, { Component } from 'react';
import DashboardList from './DashboardList';

class Overview extends Component {
    render() {
        return (<div>
            <h2>Dashboards</h2>
            <DashboardList />
        </div>
        );
    }
}

export default Overview;
