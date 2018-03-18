import React, { Component } from 'react';
import './App.css';
import Login from './login/Login';
import DashTileGrid from './overview/DashTileGrid';

class App extends Component {
  state = {
    username: '',
    password: ''
  };

  handleChange = key => event => {
    this.setState({
      [key]: event.target.value
    });
  };

  render() {
    return (
      <div className="App">
        <header className="App-header">
          <h1 className="App-title">PyDash.io Login</h1>
        </header>
        {/*<Login />*/}
        <DashTileGrid username='test-user' />
      </div>
    );
  }
}

export default App;
