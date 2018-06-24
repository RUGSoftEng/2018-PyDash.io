import React, { Component } from 'react';
import PropTypes from 'prop-types';
import { Switch, Route } from 'react-router-dom';

import LoginPage from './login/LoginPage';
import RegistrationPage from './registration/RegistrationPage';
import AuthenticatedApp from './authenticated_app/AuthenticatedApp';
import VerificationPage from './registration/VerificationPage';

/**
 * Will dispatch between the various top-level routes that the application uses.
 *
 * After having logged in, there are various sub-routes, which are dispatched in their own component, inside of AuthenticatedApp.
 */
class Routes extends Component {
    render = () => {
        return (
            <Switch>
                <Route exact path='/' render={(props) => (
                    <LoginPage
                        signInHandler={this.props.signInHandler}
                        {...props}
                    />
                )}/>
                <Route exact path='/register' render={(props) => (
                    <RegistrationPage
                        username={this.props.username}
                        isAuthenticated={this.props.isAuthenticated}
                        {...props}
                    />
                )}/>
                <Route exact path={'/verify/:verification_code'} render={ ({match}) => (
                    <VerificationPage verification_code={match.params.verification_code} />
                )} />
                <Route path='/overview' render={(props) => (
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
