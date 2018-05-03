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
            <BreadcrumbRoute path='/overview' title='Overview' render={ ({ match }) => (
                <div>
                    <Route exact path={match.url + '/'} component={() => (<OverviewPage dashboards={this.props.dashboards} />)} />
                    <BreadcrumbRoute exact path={match.url + '/settings'} component={SettingsPage} title='Settings' />
                    <BreadcrumbRoute path={match.url + '/dashboards/'} isLink={false} title='Dashboards' render={ ({ match }) => (
                        <Route path={match.url + '/:id'} render={ ({match}) => {
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
    dashboards: PropTypes.object.isRequired,
};


export default AuthenticatedRoutes;
