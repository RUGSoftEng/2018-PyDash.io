import React, { Component } from 'react';
import PropTypes from 'prop-types';

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

class Logout extends Component {
    state = {
        success: false
    };

    handleChange = key => event => {
        this.setState({
            [key]: event.target.value
        });
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
        return this.state.success ? (
            <Redirect to="/" />
        ) : (
            <ListItem button onClick={this.logout}>
                <ListItemIcon>
                    <ExitToApp />
                </ListItemIcon>
                <ListItemText primary="Logout" />
            </ListItem>
        );
    }
}

Logout.propTypes = {
    signOutHandler: PropTypes.func.isRequired,
};

export default Logout;
