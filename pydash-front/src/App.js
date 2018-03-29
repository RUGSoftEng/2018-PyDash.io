import React, { Component } from 'react';
import './App.css';
import Login from './login/Login';
import Dashboard from './dashboard/Dashboard';
import Overview from './overview/Overview';
import { Switch, Route } from 'react-router-dom'

class App extends Component {
  render() {
    return (
      <div className="App">
        <Switch>
          <Route exact path='/' component={Login} />
          <Route exact path='/dashboard' component={Dashboard} />
          <Route path='/overview' component={Overview} />
        </Switch>
      </div>
    );
  }
}

export default App;
