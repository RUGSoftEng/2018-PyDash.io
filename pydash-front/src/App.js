import React, { Component } from 'react';
import './App.css';
import Login from './login/Login';
import Dashboard from './app/dashboard/Dashboard';
import { Switch, Route } from 'react-router-dom';
import IsLoggedIn from './login/IsLoggedIn';

class App extends Component {
    state = {
        username: '',
        loggedIn: IsLoggedIn
    };

    changeUsername = (username) => {
        console.log(username);
        this.setState({
            username: username
        });
    };


  render() {
    return (
      <div className="App">
        <p>LOGGED IN: {this.state.loggedIn}</p>
        <Switch>
          {/* `exact` because its only one slash */}
          <Route exact path='/' render={(props) => <Login changeUsernameHandler={this.changeUsername} {...props} />} />
          <Route path='/dashboard' render={(props) => <Dashboard username={this.state.username} {...props} /> } />
        </Switch>
      </div>
    );
  }
}

export default App;
