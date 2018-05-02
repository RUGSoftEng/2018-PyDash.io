import React, { Component } from 'react';
import PropTypes from 'prop-types';

// Routing:
import { Route } from 'react-router-dom';
import BreadcrumbRoute from '../common/BreadcrumbRoute';

// Contents:
import Overview from './overview/Overview';
import DashboardRoutes from './dashboard/DashboardRoutes';
import Settings from './settings/Settings';


class AuthenticatedRoutes extends Component {
    render = () => {
        return (
            <BreadcrumbRoute path='/dashboard' title='Overview' render={ ({ match }) => (
                <div>
                    <Route exact path={match.url + '/'} component={() => (<Overview dashboards={this.props.dashboards} />)} />
                    <BreadcrumbRoute exact path={match.url + '/settings'} component={Settings} title='Settings' />
                    <Route path={match.url + '/view/'} title='Dashboard' render={ ({ match }) => (
                        <Route path={match.url + '/:id'} render={ ({match}) => {
                                console.log("ROUTE MATCH:", match);
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
