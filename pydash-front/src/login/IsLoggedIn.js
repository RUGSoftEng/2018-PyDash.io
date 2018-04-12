import axios from 'axios';

function isLoggedIn() {
    return axios('http://localhost:5000/api/login', {
        method: 'post',
        withCredentials: true
    }).then((response) => {
        console.log('got diz', response);
        return true;
    }).catch((error) => {
        console.log('error', error);
        return false;
    });
}

export default {
    loggedIn: isLoggedIn()
};