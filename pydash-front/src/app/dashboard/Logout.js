import React, { Component } from 'react';
import { Redirect } from 'react-router'
import { ListItem, ListItemIcon, ListItemText } from 'material-ui/List';
import ExitToApp from 'material-ui-icons/ExitToApp';
import axios from 'axios';

class Login extends Component {
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
        console.log('logging out');
        // axios.get('http://localhost:5000/api/dashboards/', {
        //     withCredentials: true
        // }).then((response) => {
        //     console.log(response);
        // }).catch((error) => {
        //     console.log(error);
        // });

        // Make a request for a user with a given ID
        axios('http://localhost:5000/api/logout', {
            method: 'post',
            withCredentials: true
        }).then((response) => {
            console.log(response);
            this.setState(prevState => ({success: true}))
        }).catch((error) => {
            console.log(error);
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

export default Login;
