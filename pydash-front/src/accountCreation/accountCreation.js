import React, { Component } from 'react';
import { Redirect } from 'react-router'
import Button from 'material-ui/Button';
import TextField from 'material-ui/TextField';
import axios from 'axios';
import Logo from '../images/logo.png'

class accountCreation extends Component {
    state = {
        username: '',
        password: '',
        Confirmpassword: '',
        email: '',
        error: false,
        message: '',
        success: false
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
        axios.post('http://localhost:5000/api/login', {
            username,
            password},
            {withCredentials: true}
        ).then((response) => {
            console.log(response);
            this.props.changeUsernameHandler(username)
            this.setState(prevState => ({
                error: false,
                helperText: '',
                success: true
            }));
        }).catch((error) => {
            console.log(error);
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
                        label="Choose username"
                        value={this.state.username}
                        onChange={this.handleChange('username')}
                        margin="normal"
                        error={this.state.error}
                    />
                    <br />
                    <TextField
                        id="Email"
                        label="email"
                        value={this.state.email}
                        onChange={this.handleChange('email')}
                        margin="normal"
                        
                    />
                    <br />
                    
                    <TextField
                        id="Password"
                        label="Password"
                        value={this.state.password}
                        onChange={this.handleChange('password')}
                        margin="normal"
                        type="password"
                        error={this.state.error}
                        helperText={this.state.helperText}
                    />
                    <br />
                    <TextField
                        id="Confirmpassword"
                        label="Confirm password"
                        value={this.state.Confirmpassword}
                        onChange={this.handleChange('password')}
                        margin="normal"
                        type="password"
                        
                    />
                    <br />
                    <p>
                    <Button type="submit" variant="raised" color="primary" href="/dashboard">
                        Register
                    </Button>
                    </p>
                </form>
            </div>
        );
    }
}

export default accountCreation;
