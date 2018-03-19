import React, { Component } from 'react';
import './App.css';
import Login from './login/Login';
import DashTileGrid from './overview/DashTileGrid';
import { Switch, Route } from 'react-router-dom'

class App extends Component {
  state = {
    loggedIn: false
  };

  handleChange = key => event => {
    this.setState({
      [key]: event.target.value
    });
  };

  render() {
    return (
      <div className="App">
        <Switch>
          <Route exact path='/' component={DashTileGrid} />
          <Route path='/login' component={Login} />
        </Switch>
      </div>
    );
  }
}

export default App;
