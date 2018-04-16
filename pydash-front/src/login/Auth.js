import axios from 'axios';


class Auth{
    constructor() {
        this.peek = false;
    }

    doPeek() {
        return axios('http://localhost:5000/api/login', {
            method: 'post',
            withCredentials: true
        }).then((response) => {
            console.log('got diz', response);
            this.loggedIn = true;
        }).catch((error) => {
            console.log('error', error);
            this.loggedIn = false;
        });
    }

    get isLoggedIn() {
        if (!this.peek) {
            this.doPeek();
            this.peek = true;
        }

        return this.loggedIn;
    }

    set isLoggedIn(val) {
        this.loggedIn = val;
    }
};

export default new Auth();