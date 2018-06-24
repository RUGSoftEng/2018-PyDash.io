import React, { Component } from 'react';

import axios from 'axios';

import Logo from '../images/logo.png';

/**
 * Renders the verification page new accounts are sent to after clicking on the vericiation link in their e-mail
 * . 
 */
class VerificationPage extends Component {
    state = {
        message: 'Loading'
    }

    componentDidMount() {
        if (!this.props.verification_code) {
            this.setState(prevState => {
                return ({
                    ...prevState,
                    message: 'No verification code present',
                });
            });
        } else {
            let verification_code = this.props.verification_code;
            axios.post(window.api_path + '/api/user/verify', {
                verification_code
            }).then((response) => {
                console.log(response);
                this.setState(prevState => {
                    return {
                        ...prevState,
                        message: response.data.message
                    };
                });
            }).catch((error) => {
                console.log(error);
                this.setState(prevState => {
                    if (error.response.data.message !== null) {
                        console.log(error.response.data);
                        return {
                            ...prevState,
                            message: error.response.data.message
                        };
                    } else {
                        return {
                            ...prevState,
                            message: 'Unspecified error'
                        }
                    }
                });
            })
        }
    }

    render = () => {
        return (
            <div>
                <header className="App-header">
                    <img alt="PyDash logo" width="200" src={Logo} />
                </header>
                <h4>
                    <em>
                        {this.state.message}
                    </em>
                </h4>
            </div>
        );
    }
}

export default VerificationPage;