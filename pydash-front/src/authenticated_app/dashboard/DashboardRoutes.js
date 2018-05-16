import React, { Component } from 'react';
import PropTypes from 'prop-types';
import _find from 'lodash-es/find';

// Routing:
import { Switch } from 'react-router-dom';
import { Route } from 'react-router-dom';
import BreadcrumbRoute from '../../common/BreadcrumbRoute';
import Endpoint from '../endpoint/Endpoint';
// Contents:
import StatisticsPage from './statistics_page/StatisticsPage';


const MatchedStatisticsPage = (props) => {
    console.log("MatchedStatisticsPage props: ", props, props.dashboard)
    if(props.dashboard === undefined){
        return () => ('');
    }
    return () => (<StatisticsPage dashboard={props.dashboard} />);
}


class DashboardRoutes extends Component {
    render = () => {
        return (
            <BreadcrumbRoute
                path={this.props.match.url}
                title={(this.props.dashboard ? (this.props.dashboard.name ? this.props.dashboard.name : this.props.dashboard.url) : '')}
                render = { ({match}) => (
                    <Switch>
                        <Route exact path={match.url + '/'} component={MatchedStatisticsPage({dashboard: this.props.dashboard})}/>
                        <BreadcrumbRoute path={match.url + '/endpoints/'} isLink={false} title='Endpoints' render={ ({match}) => (
                            <Route path={match.url + '/:endpoint_name'} render={ ({match}) => {
                                    if(this.props.dashboard!=null){
                                        const endpoint_info = _find(this.props.dashboard.endpoints, (endpoint) => (endpoint.name === match.params.endpoint_name))
                                        if(endpoint_info === undefined){
                                            return '';
                                        }
                                        return (
                                            <BreadcrumbRoute
                                                path={match.url}
                                                     title={endpoint_info.name}
                                                     render = {(_) => (
                                                         <Endpoint endpointData={endpoint_info}/>
                                                     )}
                                            />
                                        )
                                    }
                            }} />
                        )}/>
                    </Switch>
                )}/>
        );
    }
}

DashboardRoutes.propTypes = {
    dashboard: PropTypes.shape({
        id: PropTypes.string.isRequired,
        url: PropTypes.string.isRequired,
    }),
    match: PropTypes.shape({
        url: PropTypes.string.isRequired
    })
}

export default DashboardRoutes;
