import React, { Component } from 'react';
import PropTypes from 'prop-types';
import { withStyles } from 'material-ui/styles';

import axios from 'axios';

// Routing:
import { Redirect } from 'react-router'
import NavLink from 'react-router-dom/NavLink';

// Visual:
import Button from 'material-ui/Button';
import TextField from 'material-ui/TextField';
import Logo from '../images/logo.png';
import Snackbar from 'material-ui/Snackbar';
import IconButton from 'material-ui/IconButton';
import CloseIcon from '@material-ui/icons/Close';
import Warning from '@material-ui/icons/Warning';

// Sound:
import {Howl} from 'howler';
import login_soundfile from "./boot.mp3";


const login_sound = new Howl({
    src: [login_soundfile],
});

const styles = theme => ({
    close: {
      width: theme.spacing.unit * 4,
      height: theme.spacing.unit * 4,
    },
  });

class LoginPage extends Component {
    state = {
        username: '',
        password: '',
        error: false,
        message: '',
        success: false,
        loading: false,
        open: false,
        IsPasswordTooShort: true,
    };

    handleChange = key => event => {
        let target_val = event.target.value;
        this.setState((prevState) => {
            let isPasswordUnsafe = prevState.isPasswordUnsafe;
            if(key === 'password') {
                console.log("TETS")
                // Only bug person once password is longer than eight characters
                // because that is a requirement in any case.
                isPasswordUnsafe = (target_val.length < 12 && target_val.length > 8);
            }
            return {
                [key]: target_val,
                isPasswordUnsafe: isPasswordUnsafe,
            }
        });
    };


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
                helperText: 'Both fields are required!',
            }))

            return;
        }

        this.setState(prevState => ({
            ...prevState,
                error: false,
                helperText: '',
                loading: true,
            }))


        // Make a request for a user with a given ID
        axios.post(window.api_path + '/api/login', {
            username,
            password},
            {withCredentials: true},
        ).then((response) => {
            console.log(response);
            login_sound.play()
            this.props.signInHandler(username)
            /* this.setState(prevState => ({
             *     error: false,
             *     helperText: '',
             *     success: true,
             *     loading: false
             * }));*/
        }).catch((error) => {
            console.log(error);
            if(error.response && error.response.status === 401) {
                this.setState(prevState => ({
                    error: true,
                    helperText: 'Incorrect credentials 😱',
                    loading: false,
                }))
            } else {
                this.setState(prevState => ({
                    error: true,
                    helperText: 'Unknown error returned:' + error,
                    loading: false,
                }))
            }
        });
    }

    render() {
        const { classes } = this.props;
        return this.state.success ? (
            <Redirect to="/overview" />
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
            {(this.state.isPasswordUnsafe ?
              <p className="password-safety-warning" >
                  <Warning /><br/>
                  Warning! Your password is shorter than 12 characters, which is considered unsafe.<br/>
                  Please improve your password strength on the settings page after logging in.
              </p>
            : ""
            )}
                    <p>
                    <Button  type="submit" variant="raised" color="primary" disabled={this.state.loading} onClick={ this.handleClick}>
                        {this.state.loading ? "Logging in..." : "Login"} 
                    </Button>
                    </p>
                    <p>
                    <Button component={NavLink} to="/register">Create an account?</Button>
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
                            message={<span id="message-id">Logging in</span>}
                            action={[
                            <IconButton
                                key="close"
                                aria-label="Close"
                                color="inherit"
                                className={classes.close}
                                onClick={this.handleClose}
                            >
                                <CloseIcon />
                            </IconButton>
                            ]}
                />

                </form>
            </div>
        );
    }
}
LoginPage.propTypes = {
    signInHandler: PropTypes.func.isRequired,
    classes: PropTypes.object.isRequired,
};

export default withStyles(styles)(LoginPage);
