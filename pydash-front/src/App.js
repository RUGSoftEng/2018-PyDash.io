import React, { Component } from 'react';
import logo from './logo.svg';
import './App.css';
import Button from 'material-ui/Button';
import TextField from 'material-ui/TextField';

let name = 'hhaha'

class App extends Component {
  state = {
    name: 'Jeroen Overschie'
  };

  handleChange = name => event => {
    this.setState({
      [name]: event.target.value,
    });
  };

  render() {
    return (
      <div className="App">
        <header className="App-header">
          <img src={logo} className="App-logo" alt="logo" />
          <h1 className="App-title">PyDash.io Login page</h1>
        </header>
        <p className="App-intro">
          Example react page ⚡️
          {name}
        </p>
        <Button variant="raised" color="primary">
          Hello World
        </Button>

        <br/>
        <TextField
          id="name"
          label="Name"
          value={this.state.name}
          onChange={this.handleChange('name')}
          margin="normal"
        />
        {this.state.name}
      </div>
    );
  }
}

export default App;
