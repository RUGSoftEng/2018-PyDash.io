import React, { Component } from 'react';
import PropTypes from 'prop-types';

// Routing:
import { Switch } from 'react-router-dom';
import { Route } from 'react-router-dom';
import BreadcrumbRoute from '../../common/BreadcrumbRoute';
import Endpoint from '../endpoint/Endpoint';
import { Link } from 'react-router-dom'
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
            <Switch>
             <BreadcrumbRoute path={this.props.match.url + '/endpoints/'} isLink={false} title='Endpoints' render={ ({match}) => (
                        <Route path={match.url + '/:id'} render={ ({match}) => {
                                if(this.props.dashboard!=null){
                                    for(var i = 0;i<this.props.dashboard.endpoints.length;i++){
                                        if(match.params.id===this.props.dashboard.endpoints[i].name){
                                            const endpoint_info = this.props.dashboard.endpoints[i];
                                            console.log(endpoint_info);
                                            return <Endpoint endpointData={endpoint_info}/>
                                        }
                                    }
                                }
                                console.log('Endpoint not found');
                                return <Endpoint/>
                        }} />
                    )}/>
            <BreadcrumbRoute
                path={this.props.match.url + '/'}
                title={(this.props.dashboard ? (this.props.dashboard.name ? this.props.dashboard.name : this.props.dashboard.url) : '')}
                component={MatchedStatisticsPage({dashboard: this.props.dashboard})}
            />
            </Switch>
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
