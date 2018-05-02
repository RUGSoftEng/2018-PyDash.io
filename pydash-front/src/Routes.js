import React, { Component } from 'react';
import PropTypes from 'prop-types';
import { Switch, Route } from 'react-router-dom';

import Login from './login/Login';
import AccountCreation from './accountCreation/AccountCreation';
import AuthenticatedApp from './authenticated_app/AuthenticatedApp';

class Routes extends Component {
    render = () => {
        return (
            <Switch>
                <Route exact path='/' render={(props) => (
                    <Login
                        signInHandler={this.props.signInHandler}
                        {...props}
                    />
                    )}/>
                <Route exact path='/register' render={(props) => (
                    <AccountCreation
                        username={this.props.username}
                        isAuthenticated={this.props.isAuthenticated}
                        {...props}
                    />
                )}/>
                <Route path='/dashboard' render={(props) => (
                    <AuthenticatedApp
                        username={this.props.username}
                        isAuthenticated={this.props.isAuthenticated}
                        signOutHandler={this.props.signOutHandler}
                        {...props}
                    />
                )}/>
            </Switch>
        );
    }
}

Routes.propTypes = {
    username: PropTypes.string,
    isAuthenticated: PropTypes.bool.isRequired,
    signInHandler: PropTypes.func.isRequired,
    signOutHandler: PropTypes.func.isRequired,
};

export default Routes;
