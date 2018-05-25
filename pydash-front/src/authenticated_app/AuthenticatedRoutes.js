import React, { Component } from 'react';
import PropTypes from 'prop-types';

// Routing:
import { Route } from 'react-router-dom';
import BreadcrumbRoute from '../common/BreadcrumbRoute';

// Contents:
import DashboardRoutes from './dashboard/DashboardRoutes';
import OverviewPage from './overview/OverviewPage';
import SettingsPage from './settings/SettingsPage';


class AuthenticatedRoutes extends Component {
    render = () => {
        return (
            <BreadcrumbRoute path='/overview' title='Dashboards' render={ ({ match }) => (
                <div>
                    <Route exact path={match.url + '/'} component={() => (<OverviewPage dashboards={this.props.dashboards} />)} />
                    <BreadcrumbRoute exact path={match.url + '/settings'} component={() => (<SettingsPage username={this.props.username} />)} title='Settings' />
                    <Route path={match.url + '/dashboards/'} render={ ({ match }) => (
                        <Route path={match.url + '/:id'} render={ ({match}) => {
                                if(this.props.dashboards === null){
                                    return (<em>Loading...</em>)
                                }
                                const dashboard_info = this.props.dashboards[match.params.id];
                                return <DashboardRoutes match={match} dashboard={dashboard_info}/>
                        }} />
                    )}/>
                </div>
            )} />
        );
    }
}

AuthenticatedRoutes.propTypes = {
    dashboards: PropTypes.object,
};


export default AuthenticatedRoutes;
