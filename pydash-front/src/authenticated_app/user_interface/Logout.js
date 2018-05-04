import React, { Component } from 'react';
import PropTypes from 'prop-types';
import { withStyles } from 'material-ui/styles';
import Button from 'material-ui/Button';
import Snackbar from 'material-ui/Snackbar';
import IconButton from 'material-ui/IconButton';
import CloseIcon from '@material-ui/icons/Close';
import axios from 'axios';

// Routing:
import { Redirect } from 'react-router'

// Visual:
import { ListItem, ListItemIcon, ListItemText } from 'material-ui/List';
import ExitToApp from 'material-ui-icons/ExitToApp';

// Sound:
import {Howl} from 'howler';
import logout_soundfile from './pop.mp3';


const logout_sound = new Howl({
    src: [ logout_soundfile],
});
    function sleep(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }
const styles = theme => ({
    close: {
      width: theme.spacing.unit * 4,
      height: theme.spacing.unit * 4,
    },
  });


class Logout extends Component {
    state = {
        success: false,
        open: false,
    };

    handleChange = key => event => {
        this.setState({
            [key]: event.target.value
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

    logout = (e) => {
        e.preventDefault()

        // Make a request for a user with a given ID
        axios(window.api_path + '/api/logout', {
            method: 'post',
            withCredentials: true
        }).then((response) => {
            console.log(response);
            logout_sound.play();
            this.setState(prevState => ({success: true}))
            this.props.signOutHandler();
        }).catch((error) => {
            console.log(error);
            // Also log out on error.
            this.setState(prevState => ({success: true}))
            this.props.signOutHandler();
        });
    }

    render() {
        const { classes } = this.props;
        return this.state.success ? (
         <Redirect to="/" />
             ) : (

            <div  button onClick={ this.handleClick}>
            <ListItem button onClick={this.logout}>
                <ListItemIcon >
                    <ExitToApp />
                </ListItemIcon>
               <ListItemText primary="Logout" />
            </ListItem>
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
                message={<span id="message-id">Logging out</span>}
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
            </div>
          );
    }
}

Logout.propTypes = {
    signOutHandler: PropTypes.func.isRequired,
    classes: PropTypes.object.isRequired,
};

export default withStyles(styles)(Logout);
