import React, { Component } from 'react';
import './App.css';
import Login from './login/Login';

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
        <Login />
      </div>
    );
  }
}

export default App;
