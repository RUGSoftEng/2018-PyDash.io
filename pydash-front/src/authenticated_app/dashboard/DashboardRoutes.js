import React, { Component } from 'react';
import PropTypes from 'prop-types';

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
            <BreadcrumbRoute path='/overview' title='Overview' render={ ({ match }) => (
                <div>
                    <Switch>
                        <BreadcrumbRoute
                            path={this.props.match.url + '/'}
                            title={(this.props.dashboard ? (this.props.dashboard.name ? this.props.dashboard.name : this.props.dashboard.url) : '')}
                            component={MatchedStatisticsPage({dashboard: this.props.dashboard})}
                            
                        />
                        <BreadcrumbRoute exact path={match.url + '/endpoint'} component={Endpoint} title='end' />
                    </Switch>
                </div>
            )} />
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
