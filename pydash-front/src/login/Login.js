import React, { Component } from 'react';
import './Login.css';
import Button from 'material-ui/Button';
import TextField from 'material-ui/TextField';
import axios from 'axios';

class Login extends Component {
    state = {
        username: '',
        password: '',
        error: false,
        message: ''
    };

    handleChange = key => event => {
        this.setState({
            [key]: event.target.value
        });
    };

    tryLogin = (e) => {
        e.preventDefault()
        let username = this.state.username,
            password = this.state.password
        
        if (!(username.trim()) || !(password.trim())) {
            return;
        }

        // Make a request for a user with a given ID
        axios.post('http://localhost:5000/api/login/', {
            username,
            password
        }).then((response) => {
            console.log(response);
            console.log(response.data)
            this.setState(prevState => ({
                error: false,
                helperText: ''
            }))
        })
        .catch((error) => {
            console.log(error);
            this.setState(prevState => ({
                error: true,
                helperText: 'Incorrect credentials 😱'
            }))
        });
    }

    render() {
        return (
            <div>
                <header className="App-header">
                    <h1 className="App-title">PyDash.io Login</h1>
                </header>

                <form onSubmit={this.tryLogin}>
                    <br />
                    <TextField
                        id="username"
                        label="Username"
                        value={this.state.username}
                        onChange={this.handleChange('username')}
                        margin="normal"
                        error={this.state.error}
                    />
                    <br />
                    <TextField
                        id="password"
                        label="Password"
                        value={this.state.password}
                        onChange={this.handleChange('password')}
                        margin="normal"
                        type="password"
                        error={this.state.error}
                        helperText={this.state.helperText}
                    />
                    <p>
                    <Button type="submit" variant="raised" color="primary">
                        Login
                    </Button>
                    </p>
                </form>
            </div>
        );
    }
}

export default Login;
