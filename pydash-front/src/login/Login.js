import React, { Component } from 'react';
import './Login.css';
import Button from 'material-ui/Button';
import TextField from 'material-ui/TextField';

class Login extends Component {
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
            <form>
                <br />
                <TextField
                    id="username"
                    label="Username"
                    value={this.state.username}
                    onChange={this.handleChange('username')}
                    margin="normal"
                />
                <br />
                <TextField
                    id="password"
                    label="Password"
                    value={this.state.password}
                    onChange={this.handleChange('password')}
                    margin="normal"
                    type="password"
                />
                <p>
                    <Button variant="raised" color="primary">
                        Login
                    </Button>
                </p>
            </form>
        );
    }
}

export default Login;
