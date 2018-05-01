import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import App from './App';
import { BrowserRouter } from 'react-router-dom'

// Make API host path configurable to ensure the application also works well
// while testing locally on a different port than the back-end application.
window.api_path = "";
if(window.location.host === "localhost:3000") {
    window.api_path = window.location.protocol + "//localhost:5000";
}

ReactDOM.render((
    <BrowserRouter>
        <App />
    </BrowserRouter>
), document.getElementById('root'));
