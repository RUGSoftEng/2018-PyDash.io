import React, { Component } from 'react';
import { Redirect } from 'react-router'
import Button from 'material-ui/Button';
import TextField from 'material-ui/TextField';
import axios from 'axios';
import Logo from '../images/logo.png'

class accountCreation extends React.Component {
    constructor(props) {
      super(props);
      this.state = {
        username: '',
        email: '',
        password: '',
        Confirmpassword: '',
        message: '',
        error: false,
        loading: false,
        success: false
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

   
   
   
    tryLogin = (e) => {
        e.preventDefault()
        let username = this.state.username,
            password = this.state.password
            
        if (!(username.trim()) || !(password.trim())) {
            this.setState(prevState => ({
                ...prevState,
                error: true,
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

        axios.post(window.api_path + '/api/register_user', {
            username,
            password},
            {withCredentials: true}
        ).then((response) => {
            console.log(response);
            this.props.changeUsernameHandler(username)
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
        return this.state.success ? (
            <Redirect to="/dashboard" />
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
                        error={this.state.error}
                    />
                    <br />
                    <TextField
                        id="Email"
                        label="Email"
                        value={this.state.email}
                        onChange={this.handleChange('email')}
                        margin="normal"
                        error={this.state.error}
                    />
                    <br />
                    
                    <TextField
                        id="Password"
                        label="Password"
                        value={this.state.password}
                        onChange={this.handleChange('password')}
                        margin="normal"
                        type="password"
                        error={this.state.error}

                    />
                    <br />
                    <TextField
                        id="Confirmpassword"
                        label="Confirm password"
                        value={this.state.Confirmpassword}
                        onChange={this.handleChange('Confirmpassword')}
                        margin="normal"
                        type="password"
                        error={this.state.error}
                        helperText={this.state.helperText}
                    />
                    <br />
                    <p>
                    <Button type="submit" variant="raised" color="primary" disabled={this.state.loading}>
                        {this.state.loading ? "Creating account" : "REGISTER"}
                    </Button>
                    </p>
                </form>
            </div>
        );
    }
}

export default accountCreation;

// import React from 'react';
// import TextField from 'material-ui/TextField';

// class SignupForm extends React.Component {
//   constructor(props) {
//     super(props);
//     this.state = {
//       username: '',
//       email: '',
//       password: '',
//       passwordConfirmation: '',
//       errors: {},
//       isLoading: false,
//       invalid: false
//     }

//     this.onChange = this.onChange.bind(this);
//     this.onSubmit = this.onSubmit.bind(this);
//     this.checkUserExists = this.checkUserExists.bind(this);
//   }

//   onChange(e) {
//     this.setState({ [e.target.name]: e.target.value });
//   }


//   checkUserExists(e) {
//     const field = e.target.name;
//     const val = e.target.value;
//     if (val !== '') {
//       this.props.isUserExists(val).then(res => {
//         let errors = this.state.errors;
//         let invalid;
//         if (res.data.user) {
//           errors[field] = 'There is user with such ' + field;
//           invalid = true;
//         } else {
//           errors[field] = '';
//           invalid = false;
//         }
//         this.setState({ errors, invalid });
//       });
//     }
//   }

//   onSubmit(e) {
//     e.preventDefault();

//     if (this.isValid()) {
//       this.setState({ errors: {}, isLoading: true });
//       this.props.userSignupRequest(this.state).then(
//         () => {
//           this.props.addFlashMessage({
//             type: 'success',
//             text: 'You signed up successfully. Welcome!'
//           });
//           this.context.router.push('/');
//         },
//         (err) => this.setState({ errors: err.response.data, isLoading: false })
//       );
//     }
//   }

//   render() {
//     const { errors } = this.state;
//     return (
//       <form onSubmit={this.onSubmit}>
//         <h1>Join our community!</h1>

//         <TextField
//           error={errors.username}
//           label="Username"
//           onChange={this.onChange}
//           checkUserExists={this.checkUserExists}
//           value={this.state.username}
//           field="username"
//         />

//         <TextField
//           error={errors.email}
//           label="Email"
//           onChange={this.onChange}
//           checkUserExists={this.checkUserExists}
//           value={this.state.email}
//           field="email"
//         />

//         <TextField
//           error={errors.password}
//           label="Password"
//           onChange={this.onChange}
//           value={this.state.password}
//           field="password"
//           type="password"
//         />

//         <TextField
//           error={errors.passwordConfirmation}
//           label="Password Confirmation"
//           onChange={this.onChange}
//           value={this.state.passwordConfirmation}
//           field="passwordConfirmation"
//           type="password"
//         />

//         <div className="form-group">
//           <button disabled={this.state.isLoading || this.state.invalid} className="btn btn-primary btn-lg">
//             Sign up
//           </button>
//         </div>
//       </form>
//     );
//   }
// }


// export default SignupForm;
