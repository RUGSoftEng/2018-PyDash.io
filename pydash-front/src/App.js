import React, { Component } from 'react';
import './App.css';
import Login from './login/Login';
import Dashboard from './app/dashboard/Dashboard';
import { Switch, Route } from 'react-router-dom';
import ProtectedRoute from './login/ProtectedRoute'

class App extends Component {
  state = {
      username: ''
  };

  changeUsername = (username) => {
      this.setState({
          username: username
      });
  };

  render() {
    return (
      <div className="App">
        <Switch>
          {/* `exact` because its only one slash */}
          <Route exact path='/' render={(props) => <Login changeUsernameHandler={this.changeUsername} {...props} />} />
          <ProtectedRoute path='/dashboard' render={(props) => <Dashboard username={this.state.username} {...props} />}/> 
        </Switch>
      </div>
    );
  }
}

export default App;
