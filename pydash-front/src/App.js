import React, { Component } from 'react';
import PropTypes from 'prop-types';

import { Redirect } from 'react-router'

import './App.css';
import Routes from './Routes'
import Notifier, { showNotification } from './Notifier'


/**
 * The entry point of the React application.
 * Almost all work is delegated to subcomponents.
 * The only work that the App component itself does, is to check if the user is logged in or not,
 * and pass functions to lower-level components to sign a user in or out.
 */
class App extends Component {
    state = {
        username: ''
    };

    componentWillMount = () => {
        this.setState({
            isAuthenticated: this.props.isAuthenticated,
            username: this.props.username
        })
        console.log("App state: ", this.state, this.props);
    }

    signInHandler = (username) => {
        this.setState({
            username: username,
            isAuthenticated: true
        });
        showNotification({ message: "Logged in successfully!"});
    };

    signOutHandler = () => {
        this.setState({
            username: '',
            isAuthenticated: false
        })
        showNotification({ message: "Logged out successfully!"});
    }

    redirectBasedOnAuthentication = () => {
        if(this.state.isAuthenticated && window.location.pathname === "/"){
            return <Redirect to='/overview' />;
        }

        if(!this.state.isAuthenticated && (window.location.pathname !== "/" && window.location.pathname !== '/register' && window.location.pathname.substring(0,8) !== '/verify/')){
            return <Redirect to='/' />;
        }
    }

    render() {

        return (
            <div className="App">
                {this.redirectBasedOnAuthentication()}
                <Routes
                    signInHandler={this.signInHandler}
                    signOutHandler={this.signOutHandler}
                    username={this.state.username}
                    isAuthenticated={this.state.isAuthenticated}
                />
                <Notifier />
            </div>
        );
    }
}

App.propTypes = {
    username: PropTypes.string,
    isAuthenticated: PropTypes.bool.isRequired,
};

export default App;
