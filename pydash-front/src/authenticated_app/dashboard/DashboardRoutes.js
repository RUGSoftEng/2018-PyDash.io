import React, { Component } from 'react';
import PropTypes from 'prop-types';

// Routing:
import { Switch } from 'react-router-dom';
import BreadcrumbRoute from '../../common/BreadcrumbRoute';

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
            <BreadcrumbRoute
                path={this.props.match.url + '/'}
                title={(this.props.dashboard ? this.props.dashboard.url : '')}
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
