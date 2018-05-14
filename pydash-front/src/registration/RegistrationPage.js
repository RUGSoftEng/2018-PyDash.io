import React, { Component } from 'react';
import PropTypes from 'prop-types';
import { withStyles } from 'material-ui/styles';

import { Redirect } from 'react-router'
import Button from 'material-ui/Button';
import TextField from 'material-ui/TextField';
import axios from 'axios';
import Logo from '../images/logo.png'
import Snackbar from 'material-ui/Snackbar';
import IconButton from 'material-ui/IconButton';
import CloseIcon from '@material-ui/icons/Close';



const styles = theme => ({
    close: {
      width: theme.spacing.unit * 4,
      height: theme.spacing.unit * 4,
    },
  });

class RegistrationPage extends Component {
    constructor(props) {
      super(props);
      this.state = {
        username: '',
        email: '',
        password: '',
        password_confirmation: '',
        message: '',
        error: false,
        loading: false,
          success: false,
          warnings: {},
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


    handleEmail = event => {
        const target_val = event.target.value;
        let email_warning;
        if(!/@.+?\..+/.test(target_val)){
            email_warning = "Please enter a valid e-mail address";
        }
        this.setState((prevState) => {
            let warnings = prevState.warnings
            warnings['email'] = email_warning;
            return {
                email: target_val,
                warnings: warnings,
            }
        })
    }

    handlePassword = event => {
        const target_val = event.target.value;
        let password_warning = null;
        if(target_val.length < 8){
            password_warning = "The password should be either > 8 chars, containing at least one capital and non-alphabetic char, or > 12 chars.";
        }
        this.setState((prevState) => {
            let warnings = prevState.warnings
            warnings['password'] = password_warning;
            return {
                password: target_val,
                warnings: warnings,
            }
        })
    }

    handlePasswordConfirmation = event => {
        const target_val = event.target.value;
        let password_confirmation_warning;
        if(target_val != this.state.password){
            password_confirmation_warning = "The passwords are not the same!";
        }
        this.setState((prevState) => {
            let warnings = prevState.warnings
            warnings['password_confirmation'] = password_confirmation_warning;
            return {
                password_confirmation: target_val,
                warnings: warnings,
            }
        })
    }


    handleClick = () => {
        this.setState({ open: true });
      };

      handleClose = (event, reason) => {
        if (reason === 'clickaway') {
            return;
        }
    
        this.setState({ open: false });
      };
   
   
    tryLogin = (e) => {
        e.preventDefault()
        let username = this.state.username,
            password = this.state.password
            
        if (!(username.trim()) || !(password.trim())) {
            this.setState(prevState => ({
                ...prevState,
                error: true,
                open: false,
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
        const { classes } = this.props;
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
                        error={this.state.warnings['username'] || this.state.error}
                    />
                    <br />
                    <TextField
                        id="Email"
                        label="Email"
                        value={this.state.email}
                        onChange={this.handleEmail}
                        margin="normal"
                        error={this.state.warnings['email'] || this.state.error}
                    />
                    <br />

                    <TextField
                        id="Password"
                        label="Password"
                        value={this.state.password}
                        onChange={this.handlePassword}
                        margin="normal"
                        type="password"
                        error={this.state.warnings['password'] || this.state.error}

                    />
                    <br />
                    <TextField
                        id="password_confirmation"
                        label="Confirm password"
                        value={this.state.password_confirmation}
                        onChange={this.handlePasswordConfirmation}
                        margin="normal"
                        type="password"
                        error={this.state.warnings['password_confirmation'] || this.state.error}
                        helperText={this.state.helperText}
                    />
                    <br />
                    <ul class="registration-errors">
                        {Object.keys(this.state.warnings).map(key => (
                            (this.state.warnings[key] ? <li>{this.state.warnings[key]}</li> : '')
                        ))}
                    </ul>
                    <p>
                    <Button type="submit" variant="raised" color="primary" disabled={this.state.loading}  onClick={ this.handleClick}>
                        {this.state.loading ? "Creating account" : "Register"}
                    </Button>
                    </p>
                    <Snackbar
                            anchorOrigin={{
                            vertical: 'bottom',
                            horizontal: 'left',
                            }}
                            open={this.state.open}
                            autoHideDuration={6000}
                            onClose={this.handleClose}
                            SnackbarContentProps={{
                            'aria-describedby': 'message-id',
                            }}
                            message={<span id="message-id">User registered</span>}
                            action={[
                            <IconButton
                                key="close"
                                aria-label="Close"
                                color="inherit"
                                className={classes.close}
                                onClick={this.handleClose}
                            >
                                <CloseIcon />
                            </IconButton>,
                            ]}
                />
                </form>
            </div>
        );
    }
}

RegistrationPage.propTypes = {
    signInHandler: PropTypes.func.isRequired,
    classes: PropTypes.object.isRequired,
};

export default withStyles(styles)(RegistrationPage);
