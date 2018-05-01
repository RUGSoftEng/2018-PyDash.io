import React from 'react';
import { Redirect } from 'react-router'
import Button from 'material-ui/Button';
import TextField from 'material-ui/TextField';
import axios from 'axios';
import Logo from '../images/logo.png'

class accountCreation extends React.Component {
    constructor(props) {
      super(props);
      this.state = {
        username: '',
        email: '',
        password: '',
        Confirmpassword: '',
        message: '',
        error: false,
        loading: false,
        success: false
      }

  }
  onChange(e) {
    this.setState({ [e.target.name]: e.target.value });
  }
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
                helperText: 'These fields are required!',
            }))

            return;
        }
        this.setState(prevState => ({
            ...prevState,
                error: false,
                helperText: '',
                loading: true
            }))

        axios.post(window.api_path + '/api/user/register', {
            username,
            password},
            {withCredentials: true}
        ).then((response) => {
            console.log(response);
            this.setState(prevState => ({
                error: false,
                helperText: '',
                success: true,
                loading: false
            }));
        }).catch((error) => {
            console.log(error);
            if(error.response && error.response.status === 409) {
                this.setState(prevState => ({
                    error: true,
                    helperText: 'User already exists',
                    loading: false,
                }))
            }
        });
    }

    render() {
        return this.state.success ? (
            <Redirect to="/" />
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
                        label="Email"
                        value={this.state.email}
                        onChange={this.handleChange('email')}
                        margin="normal"
                        error={this.state.error}
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

                    />
                    <br />
                    <TextField
                        id="Confirmpassword"
                        label="Confirm password"
                        value={this.state.Confirmpassword}
                        onChange={this.handleChange('Confirmpassword')}
                        margin="normal"
                        type="password"
                        error={this.state.error}
                        helperText={this.state.helperText}
                    />
                    <br />
                    <p>
                    <Button type="submit" variant="raised" color="primary" disabled={this.state.loading}>
                        {this.state.loading ? "Creating account" : "REGISTER"}
                    </Button>
                    </p>
                </form>
            </div>
        );
    }
}

export default accountCreation;