import React, { Component } from 'react';
import './App.css';
import Login from './login/Login';
import Dashboard from './app/dashboard/Dashboard';
import { Switch, Route } from 'react-router-dom';
import ProtectedRoute from './login/ProtectedRoute'
// import IsLoggedIn from './login/IsLoggedIn';
// import axios from 'axios';

class App extends Component {
  state = {
      username: '',
      // loggedIn: false,
      // didPeek: false
  };

  changeUsername = (username) => {
      this.setState({
          username: username
      });
  };

  // get isLoggedIn() {
  //   if (this.state.didPeek) {
  //     this.peek();
  //     this.state.didPeek = true;
  //   }

  //   return this.state.loggedIn;
  // }

  // peek = () => {
  //   axios('http://localhost:5000/api/login', {
  //     method: 'post',
  //     withCredentials: true
  //   }).then((response) => {
  //     console.log('got diz', response);
  //     this.state.loggedIn = true;
  //   }).catch((error) => {
  //     console.log('error', error);
  //     this.state.loggedIn = false;
  //   });
  // }
  
  // requireAuth(nextState, replace) {
  //   if (!IsLoggedIn.isLoggedIn()) {
  //     replace({
  //       pathname: '/'
  //     })
  //   }
  // }

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
