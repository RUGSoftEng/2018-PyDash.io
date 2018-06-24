import React, { Component } from 'react';

import axios from 'axios';

// Visual:
import Button from 'material-ui/Button';
import TextField from 'material-ui/TextField';
import Dialog, {
    DialogActions,
    DialogContent,
    DialogContentText,
    DialogTitle,
} from 'material-ui/Dialog';

// Notifications
import { showNotification } from '../../Notifier'

class AddDashboardDialog extends Component {
    constructor(props) {
        super(props);
        this.state = {
            url: '',
            name: '',
            token: '',
            message: '',
            error: false,
            errorURL: false,
            errorToken: false,
            loading: false,
            success: false,
        }
    }

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

    handleSubmit = (e) => {
        this.tryCreation(e);
        //alert("Settings saved!");
      };


    preventEmpty = () =>{
        let url = this.state.url,
            token = this.state.token;
        if (!(token.trim())||!(url.trim())) {
            if(!token.trim()){
                this.setState(prevState => ({
                    ...prevState,
                    errorToken: true,
                    open: false,
                    helperText: 'These fields are required!',
                }))
            }
            if(!url.trim()){
                this.setState(prevState => ({
                    ...prevState,
                    errorURL: true,
                    open: false,
                    helperText: 'These fields are required!',
                }))
            }
            return 0;
        }
        return 1;
    }

    resetState = () => {
        this.setState(prevState => ({
            ...prevState,
            helperText: '',
            error: false,
            errorToken: false,
            errorURL: false,
        })) 
    };

    registerCall = () =>{
        let url = this.state.url,
            name = this.state.name,
            token = this.state.token;
            
        axios.post(window.api_path + '/api/dashboards/register', {
            url,
            name,
            token},
            {withCredentials: true}
        ).then((response) => {
            console.log(response);
            this.setState(prevState => ({
                ...prevState,
                helperText: '',
                success: true,
                loading: false,
            }));
            showNotification({ message: "Dashboard has been added!"});
            this.props.callBack();
        }).catch((err) => {
            console.log(err);
            console.log(err.response);
            if(err.response && err.response.status === 400) {
                this.setState(prevState => ({
                    ...prevState,
                    error: true,
                    helperText: err.response.data.message,
                    loading: false,
                }));
            }
        });
    }

    tryCreation = (e) => {
        e.preventDefault();

        if(this.preventEmpty()===0){
            return;
        }

        this.registerCall()
        this.resetState()
    }

    render() {

        return (
            <div>
                <Dialog
                    open={this.props.open}
                    onClose={this.props.onClose}
                    aria-labelledby="form-dialog-title"
                >
                    <DialogTitle id="form-dialog-title">Add new dashboard</DialogTitle>
                    <DialogContent>
                        <DialogContentText>
                            To add a new dashboard, we will need some information from you.
                        </DialogContentText>
                        <TextField
                            autoFocus
                            id="url"
                            label="Dashboard URL: https://example.com/dashboard"
                            type="url"
                            value={this.state.url}
                            fullWidth
                            required
                            error={this.state.errorURL||this.state.error}
                            onChange={this.handleChange('url')}
                        />
                        <small>This is the page at which you can access the Flask Monitoring Dashboard, without trailing slash. Unless configured otherwise, this is your domain name followed by '/dashboard'.</small>
                        <TextField
                            id="name"
                            label="Dashboard name"
                            type="text"
                            value={this.state.name}
                            fullWidth 
                            onChange={this.handleChange('name')}
                        />
                        <small>Optional. This name will be used in PyDash's interface.</small>
                        <TextField 
                            id="token"
                            label="Security token"
                            type="password"
                            value={this.state.token}
                            fullWidth 
                            required
                            error={this.state.errorToken||this.state.error}
                            helperText={this.state.helperText}
                            onChange={this.handleChange('token')}
                        />
                        <small>The Flask Monitoring Dashboard <em>security token</em> is set after importing <em>flask_monitoringdashboard</em> into your Flask application using <em>flask_monitoringdashboard.config.security_token</em>. If you are still using the default token, you are susceptible to eavesdroppers, so do not forget to change it!</small>
                         <DialogActions>
                        <Button onClick={this.props.onClose} color="default">
                            Cancel
                        </Button>
                        <Button onClick={this.handleSubmit} color="primary" disabled={this.state.loading} variant="raised">
                            {this.state.loading ? "Adding dashboard" : "Save"}
                        </Button>
                       
                    </DialogActions>
                    </DialogContent>
                    

                    
                </Dialog>
                {/* <Snackbar
                    anchorOrigin={{
                    vertical: 'bottom',
                    horizontal: 'left',
                    }}
                    open={this.state.openS}
                    autoHideDuration={6000}
                    onClose={this.handleCloseSnack}
                    ContentProps={{
                    'aria-describedby': 'message-id',
                    }}
                    message={<span id="message-id">Changes have been saved!</span>}
                    action={[
                    <IconButton
                    key="close"
                    aria-label="Close"
                    color="inherit"
                    //className={classes.close}
                    onClick={this.handleCloseSnack}
                    >
                    <CloseIcon />
                    </IconButton>,
                    ]}
                    /> */}
            </div>
        );
    }
}

export default AddDashboardDialog;
