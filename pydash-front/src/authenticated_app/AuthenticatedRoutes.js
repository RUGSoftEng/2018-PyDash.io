import React, { Component } from 'react';
import PropTypes from 'prop-types';

import { Route } from 'react-router-dom';

/* import { Breadcrumb } from 'react-breadcrumbs'*/
import BreadcrumbRoute from '../common/BreadcrumbRoute';

import Overview from './overview/Overview';
import DashboardPage from './dashboard/DashboardPage';
import Settings from './settings/Settings';

const MatchedDashboardPage = (props) => {
    console.log("MatchedDashboardPage props: ", props, props.dashboard)
    if(props.dashboard === undefined){
        return () => ('');
    }
    return () => (<DashboardPage dashboard={props.dashboard} />);
}

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
                                return (<BreadcrumbRoute
                                        path={match.url + '/'}
                                        title={(dashboard_info ? dashboard_info.url : '')}
                                        component={MatchedDashboardPage({dashboard: dashboard_info})}
                                />);
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
