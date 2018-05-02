import React, { Component } from 'react';
import './App.css';
import Login from './login/Login';
// import MainInterface from './app/main_interface/MainInterface';
import { Redirect } from 'react-router'
import { Switch, Route } from 'react-router-dom';
import MainInterface from './app/main_interface/MainInterface'
import AccountCreation from './accountCreation/AccountCreation';


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
            return <Redirect to='/dashboard' />;
        }

        if(!this.state.isAuthenticated && window.location.pathname !== "/"){
            return <Redirect to='/' />;
        }
    }

    render() {

        return (
            <div className="App">
                {this.redirectBasedOnAuthentication()}
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
                    <Route exact path='/accountCreation' render={(props) =>
                        <AccountCreation
                            username={this.state.username}
                            isAuthenticated={this.state.isAuthenticated}
                            {...props}
                        />
                    }/>
                </Switch>
            </div>
        );
    }
}

export default App;
