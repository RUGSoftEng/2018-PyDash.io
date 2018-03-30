import React, { Component } from 'react';
import './App.css';
import Login from './login/Login';
import Dashboard from './app/dashboard/Dashboard';
import { Switch, Route } from 'react-router-dom'

class App extends Component {
  render() {
    return (
      <div className="App">
        <Switch>
          {/* `exact` because its only one slash */}
          <Route exact path='/' component={Login} />
          <Route path='/dashboard' component={Dashboard} />
        </Switch>
      </div>
    );
  }
}

export default App;
