import React, { Component } from 'react';
import PropTypes from 'prop-types';

import axios from 'axios';

// Contents:
import UserInterface from './user_interface/UserInterface'
import AuthenticatedRoutes from './AuthenticatedRoutes';

/**
 * Base of the app after logging in. Renders the user interface and the relevant page for the current URL.
 * Also handles the updating of data for the dashboards linked to the logged in account. 
 * 
 */
class AuthenticatedApp extends Component {
    state = {
        dashboards: null
    }

    updateData = () => {
        axios(window.api_path + '/api/dashboards', {
          method: 'get',
          withCredentials: true
        }).then((response) => {
          console.log('found some data', response);
          if (response.data.hasOwnProperty('error')) {
            console.log("Error found");
            this.setState(prevState => {
              return {
                ...prevState,
                  dashboards: null,
                error: response.data.error,
              };
            });
          } else {
              const dashboards = response.data.reduce((accum, dashboard) => {
                  accum[dashboard.id] = dashboard;
                  return accum;
              }, {});
              console.log("DASHBOARDS DATA:", dashboards);
            this.setState(prevState => {
              return {
                ...prevState,
                dashboards: dashboards,
              };
            });
          }
        }).catch((error) => {
          console.log('error while fetching dashboards information', error);
        });
    }

    componentDidMount = () => {
        console.log("Before DashboardList endpoint call")
        this.updateData();
    }

    render = () => {
        return (
            <UserInterface
                username={this.props.username}
                signOutHandler={this.props.signOutHandler}
            >
                <AuthenticatedRoutes dashboards={this.state.dashboards} username={this.props.username} updateData={this.updateData} />
            </UserInterface>
        );
    };
}

AuthenticatedApp.propTypes = {
    username: PropTypes.string.isRequired,
    isAuthenticated: PropTypes.bool.isRequired,
    signOutHandler: PropTypes.func.isRequired,
};

export default AuthenticatedApp;
