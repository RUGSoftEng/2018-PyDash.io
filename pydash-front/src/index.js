import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import App from './App';
import { BrowserRouter } from 'react-router-dom'
import axios from 'axios';

// Make API host path configurable to ensure the application also works well
// while testing locally on a different port than the back-end application.
window.api_path = "";
if(window.location.host === "localhost:3000") {
    window.api_path = window.location.protocol + "//localhost:5000";
}

function tryLogin(){
        // Make a request for a user with a given ID
        axios.post(window.api_path + '/api/login', {},
            {withCredentials: true}
        ).then((response) => {
            console.log('person logged in', response);
            renderReact({isAuthenticated: true, username: response.data.user.username});
        }).catch((error) => {
            console.log('person not logged in', error);
            renderReact({isAuthenticated: false});
        });
}

function renderReact(startup_props){
    ReactDOM.render((
        <BrowserRouter>
            <App {...startup_props} />
        </BrowserRouter>
    ), document.getElementById('root'));
}

function startApplication(){
    tryLogin();
}

startApplication();
