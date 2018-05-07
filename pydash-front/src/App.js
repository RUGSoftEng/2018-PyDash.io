import React, { Component } from 'react';
import PropTypes from 'prop-types';

import { Redirect } from 'react-router'
<<<<<<< HEAD
import { Switch, Route } from 'react-router-dom';
import MainInterface from './app/main_interface/MainInterface'
import AccountCreation from './accountCreation/AccountCreation';
import Settings from './app/settings/Settings';
=======

import './App.css';
import Routes from './Routes'

>>>>>>> development

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
    };

    signOutHandler = () => {
        this.setState({
            username: '',
            isAuthenticated: false
        })
    }

    redirectBasedOnAuthentication = () => {
        if(this.state.isAuthenticated && window.location.pathname === "/"){
            return <Redirect to='/overview' />;
        }

        if(!this.state.isAuthenticated && (window.location.pathname !== "/" && window.location.pathname !== '/register')){
            return <Redirect to='/' />;
        }
    }

    render() {

        return (
            <div className="App">
                {this.redirectBasedOnAuthentication()}
<<<<<<< HEAD
                <Switch>
                    {/* `exact` because its only one slash */}
                    <Route exact path='/' render={(props) =>
                        <Login
                            signInHandler={this.signInHandler}
                            {...props}
                        />}
                    />
                    <Route path='/dashboard' render={(props) =>
                        <MainInterface
                            username={this.state.username}
                            isAuthenticated={this.state.isAuthenticated}
                            signOutHandler={this.signOutHandler}
                            {...props}
                        />
                    }/>
                    <Route exact path='/register' render={(props) =>
                        <AccountCreation
                            username={this.state.username}
                            isAuthenticated={this.state.isAuthenticated}
                            {...props}
                        />
                    }/>
                    <Route exact path='/dashboard/settings' render={(props) =>
                        <Settings
                        username={this.state.username}
                        isAuthenticated={this.state.isAuthenticated}
                        {...props}
                    
                        />
                    }/>
                </Switch>
=======
                <Routes
                    signInHandler={this.signInHandler}
                    signOutHandler={this.signOutHandler}
                    username={this.state.username}
                    isAuthenticated={this.state.isAuthenticated}
                />
>>>>>>> development
            </div>
        );
    }
}

App.propTypes = {
    username: PropTypes.string,
    isAuthenticated: PropTypes.bool.isRequired,
};

export default App;
