import React, { Component } from 'react';
import { Redirect } from 'react-router'
import Button from 'material-ui/Button';
import TextField from 'material-ui/TextField';
import axios from 'axios';
import Logo from '../images/logo.png';
import {Howl} from 'howler';

import login_soundfile from "./boot.mp3";

const login_sound = new Howl({
    src: [login_soundfile],
});

class Login extends Component {
    state = {
        username: '',
        password: '',
        error: false,
        message: '',
        success: false,
        loading: false
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
            this.setState(prevState => ({
                ...prevState,
                error: true,
                helperText: 'Both fields are required!',
            }))

            return;
        }

        this.setState(prevState => ({
            ...prevState,
                error: false,
                helperText: '',
                loading: true
            }))


        // Make a request for a user with a given ID
        axios.post('/api/login', {
            username,
            password},
            {withCredentials: true}
        ).then((response) => {
            console.log(response);

            login_sound.play()
            this.props.changeUsernameHandler(username)
            this.setState(prevState => ({
                error: false,
                helperText: '',
                success: true,
                loading: false
            }));
        }).catch((error) => {
            console.log(error);
            this.setState(prevState => ({
                error: true,
                helperText: 'Incorrect credentials 😱',
                loading: false,
            }))
        });
    }

    render() {
        return this.state.success ? (
            <Redirect to="/dashboard" />
        ) : (
            <div>
                <header className="App-header">
                    <img alt="PyDash logo" width="200" src={Logo} />
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
                    <Button type="submit" variant="raised" color="primary" disabled={this.state.loading}>
                        {this.state.loading ? "Logging in..." : "Login"}
                    </Button>
                    </p>
                </form>
            </div>
        );
    }
}

export default Login;
