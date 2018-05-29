import React, {Component} from 'react';
import PropTypes from 'prop-types';
import { withStyles } from 'material-ui/styles';
import ExpansionPanel, { ExpansionPanelDetails, ExpansionPanelSummary } from 'material-ui/ExpansionPanel';
import Typography from 'material-ui/Typography';
import ExpandMoreIcon from '@material-ui/icons/ExpandMore';
import { Button } from 'material-ui';
import CreateIcon from 'material-ui-icons/Create'
import DeleteIcon from 'material-ui-icons/Delete'
import Dialog, { DialogActions, DialogContent, DialogContentText, DialogTitle,} from 'material-ui/Dialog';
import TextField from 'material-ui/TextField';
import { FormControlLabel } from 'material-ui/Form';
import Switch from 'material-ui/Switch';
import { Redirect } from 'react-router'
import axios from 'axios';
import Snackbar from 'material-ui/Snackbar';
import IconButton from 'material-ui/IconButton';
import CloseIcon from '@material-ui/icons/Close';

import { showNotification } from "../../Notifier";

const styles = theme => ({
  root: {
    width: '100%',
  },
  heading: {
    fontSize: theme.typography.pxToRem(23),

    flexShrink: 0,
  },
  secondaryHeading: {
    fontSize: theme.typography.pxToRem(15),
    color: theme.palette.text.secondary,
  },
  Textpanel: {
    textAlign: 'left',
    marginLeft:'200px',
    fontSize: theme.typography.pxToRem(17),
  },
  textField: {
    marginLeft: theme.spacing.unit,
    marginRight: theme.spacing.unit,
    width: 200,
  },

  EditDeleteIcons: {
    float:"right",
  },
  button: {
    margin: theme.spacing.unit,
  },
  leftIcon: {
    marginRight: theme.spacing.unit,
  },
  rightIcon: {
    marginLeft: theme.spacing.unit,
  },
  iconSmall: {
    fontSize: 20,
  },

});

class SettingsPage extends Component {


  state = {
    username: '',
    new_username: '',
    email: this.props.email_address,
    new_email:'',
    password:'',
    new_password:'',
    current_password:'',
    passConfirm:'',
    error:false,
    open: false,
    openDeletion: false,
    checked: true,
    SoundSettings: true,
    openS: false,
    loading: false
  };
componentWillMount = () => {
    this.setState({
        isAuthenticated: this.props.isAuthenticated,
        username: this.props.username
    })
    console.log("App state: ", this.state, this.props);
}

signInHandler = (username) => {
    this.setState({
        username: username,
        isAuthenticated: true
    });
};


handleType = key => event => {
  this.setState({
      [key]: event.target.value
  });
};

handleDelete = (e) => {
  let password = this.state.password
  
  e.preventDefault()
  // Make a request for deletion
  axios.post(window.api_path + '/api/user/delete', {
    password},
    {withCredentials: true}
  ).then((response) => {
    if(this.state.password===this.state.passConfirm){     
      this.props.signOutHandler();
      // this.props.handleClick();
      return <Redirect to="/" />;
    } else {
      console.log('Passwords do not match!');
    }
  }).catch((error) => {
      console.log('Deletion failed');
      this.handleCloseDeletion();
  });
}

  handleSettings = (e) => {
    e.preventDefault()
    axios.post(window.api_path + '/api/user/change_settings', {
      username: this.state.username,

    },{
      method: 'post',
      withCredentials: true
  }).then((response) => {
      console.log(response);
      showNotification({ message: "Settings saved!"});
     return <Redirect to="/" />
  }).catch((error) => {
      console.log('changing settings failed');
      this.handleClose();
  });
}




// handleSounds = (e) => {

//   e.preventDefault()
//   let SoundSettings = this.state.SoundSettings
//       //Make a request for deletion
//           axios.post(window.api_path + '/api/user/change_settings', {
//           SoundSettings},{
//           method: 'post',
//           withCredentials: true
//       }).then((response) => {
//           console.log(response);
//         return <Redirect to="/" />
//       }).catch((error) => {
//           console.log('changing settings failed');
//           this.handleClose();
//       });
//     }
    
//     handlePassword = (e) =>{
//       e.preventDefault()
//       let new_password = this.state.new_password,
//           current_password = this.state.current_password
//           axios.post(window.api_path + '/api/user/change_password', {
//       new_password,
//       current_password,
//   },{
//       method: 'post',
//       withCredentials: true
//     }).then((response) => {
//       console.log(response);
//       return <Redirect to="/" />
//   }).catch((error) => {
//       console.log('changing password failed');
//       this.handleClose();
//   });
// }
handleClick = () => {
  this.setState({ openS: true });
  //alert("Settings saved!");
};

handleCloseSnack = (event, reason) => {
  if (reason === 'clickaway') {
    return;
  }

  this.setState({ openS: false });
};
handleOkButton = (e) => {
  e.preventDefault()
  let new_password = this.state.new_password,
      current_password = this.state.current_password
  // Make a request for deletion
  axios(window.api_path + '/api/user/change_password', {
      new_password,
      current_password,
  },{
      method: 'post',
      withCredentials: true
    }).then((response) => {
      console.log(response);
        showNotification({ message: "Password updated!"});
      return <Redirect to="/" />
  }).catch((error) => {
      console.log('changing password failed');
      this.handleClose();
  });
}
let username = this.state.new_username,
    email = this.state.new_email,
    new_password = this.state.new_password,
    current_password = this.state.current_password
    if (!(username.trim()) && !(email.trim()) && !(new_password.trim()) && !(current_password.trim())) {
      this.setState(prevState => ({
          ...prevState,
          error:true,
          snackbar:false,
          
      }))
      
      return alert("All fields cannot be empty!");
  }
      if(((username.trim())||email.trim())){
      
             this.setState(prevState => ({
              ...prevState,
              loading: true,
          }))
                axios.post(window.api_path + '/api/user/change_settings', {
                username,email},{
                method: 'post',
                withCredentials: true, 
            }).then((response) => {
              this.setState(prevState => ({
                ...prevState,
                error:true,
                snackbar:false,
                
            }))
                console.log(response);
                this.handleClose();
                window.location.reload();
            }).catch((error) => {
                this.setState(prevState => ({
                snackbar: false,
                error:true,
            }))
                console.log('changing settings failed');
                this.handleClose();
            });
          }
    else if(((new_password.trim())||current_password.trim())){

              this.setState(prevState => ({
                ...prevState,
                loading: true,
                error:false,
            }))
              axios.post(window.api_path + '/api/user/change_password', {
              new_password,
              current_password,
          },{
              method: 'post',
              withCredentials: true,
            }).then((response) => {
              console.log(response);
              this.handleClose();
              window.location.reload();
          }).catch((error) => {
            this.setState(prevState => ({
              snackbar: false,
              error:true,
          }))
          this.setState(prevState => ({
            ...prevState,
            error:true,
            snackbar:false,
            
        }))
              console.log('changing password failed');
              this.handleClose();
    });
  }
    }

  handleClickOpen = () => {
    this.setState({ open: true });
  };

  handleClose = () => {
    this.setState({ open: false });
  };

  handleClickOpenDeletion = () => {
    this.setState({ openDeletion: true });
  };

  handleCloseDeletion = () => {
    this.setState({ openDeletion: false });
  };

  handleChangeSwitch = name => event => {
    this.setState({ [name]: event.target.checked });
  };

  handleChange = key => event => {
    this.setState({
        [key]: event.target.value
    });
};
  handleSoundSettings = ()=>{
    this.setState({SoundSettings: false});
  };



  render() {
    const { classes } = this.props;

    return (

      <div className={classes.root}>
        <h2>Settings</h2>
        <ExpansionPanel>
        <ExpansionPanelSummary expandIcon={<ExpandMoreIcon />}>
            <Typography className={classes.heading}>Personal data
            </Typography>
          </ExpansionPanelSummary>
          
        <Button variant="raised" color="primary" className={classes.EditDeleteIcons} onClick={this.handleClickOpen} >
              Edit information
              <CreateIcon className={classes.rightIcon}/>
          </Button>
          <Typography className={classes.Textpanel}>
          Username: {this.props.username}
          <br/>

          Email: {this.props.email_address}
          <br/>

          Registration date:...
          </Typography>
          <div>
        <Dialog
          open={this.state.open}
          onClose={this.handleClose}
          aria-labelledby="form-dialog-title"
        >
          <DialogTitle id="form-dialog-title">Updating personal data</DialogTitle>
          <DialogContent>
            <DialogContentText>
              This form allows you to update your information
            </DialogContentText>
            <form onSubmit={this.handleOkButton}>
            <TextField
              id="Password"
              label="New password"
              onChange={this.handleType('new_password')}
              margin="normal"
              type="password"
              error={this.state.error}    
              className={classes.textField}
   
              
            />
            
            <TextField
              id="currentPassword"
              label={this.props.password}
              onChange={this.handleType('current_password')}
              margin="normal"
              type="password"
              error={this.state.error}   
              className={classes.textField}
   
            />
              <TextField
              autoFocus
              margin="dense"
              id="name"
              label={this.state.username}
              type="new_username"
              onChange={this.handleChange('new_username')}
              fullWidth
              className={classes.textField}

            />
            <TextField
              autoFocus
              margin="normal"
              id="full-width"
              label={this.state.email_address}
              type="name" 
              onChange={this.handleChange('new_email')}
              fullWidth   
              className={classes.textField}

            />
            <br/>
            <Button type="submit" onClick={this.handleClick} disabled={this.state.loading} variant="raised" color="primary" className={classes.EditDeleteIcons} >
            {this.state.loading ? "saving changes..." : "OK"} 
            </Button>
            <Button onClick={this.handleClose}  color="primary"className={classes.EditDeleteIcons}>
              Close
            </Button>
            </form>
          </DialogContent>
        </Dialog>
            
      </div>

        </ExpansionPanel>
        <ExpansionPanel>
          <ExpansionPanelSummary expandIcon={<ExpandMoreIcon />}>
            <Typography className={classes.heading}>General settings</Typography>
          </ExpansionPanelSummary>
          <ExpansionPanelDetails>
          <FormControlLabel
          control={
            <Switch
              checked={this.state.checked}
              onChange={this.handleChangeSwitch('checked')}
              value="checked"
              color="primary"
            />
          }
          label="Sound ON/OFF"
        />
          </ExpansionPanelDetails>
        </ExpansionPanel>
        <ExpansionPanel >
        <Button className={classes.button} variant="raised" color="secondary" onClick={this.handleClickOpenDeletion}>
        Delete account?
        <DeleteIcon className={classes.rightIcon} />
      </Button>
          <ExpansionPanelSummary expandIcon={<ExpandMoreIcon />}>
            <Typography className={classes.heading}>Advanced settings</Typography>
          </ExpansionPanelSummary>
          <ExpansionPanelDetails>
          </ExpansionPanelDetails>
        </ExpansionPanel>
        <div>
        <Dialog
          open={this.state.openDeletion}
          onClose={this.handleCloseDeletion}
          aria-labelledby="form-dialog-title"
        >
          <DialogTitle id="form-dialog-title">Account deletion</DialogTitle>
          <DialogContent>
            <DialogContentText>
              WARNING: This will permanently delete your account!
            </DialogContentText>
            <TextField
              autoFocus
              margin="dense"
              id="name"
              label="Password"
              onChange={this.handleType('password')}
              type="password"
            />
            <TextField
              autoFocus
              margin="dense"
              id="name"
              label="Confirm password"
              onChange={this.handleType('passConfirm')}
              type="password"           
            />
          </DialogContent>
          <DialogActions>
            <Button onClick={this.handleCloseDeletion} color="primary">
              Cancel
            </Button>
            <Button type="submit" onClick={this.handleDelete} color="primary">
              Delete
            </Button>
          </DialogActions>
        </Dialog>
        <Snackbar
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
              className={classes.close}
              onClick={this.handleCloseSnack}
            >
              <CloseIcon />
            </IconButton>,
          ]}
        />
      </div>


      </div>
      
    );
  }
}

SettingsPage.propTypes = {
  classes: PropTypes.object.isRequired,
};

export default withStyles(styles)(SettingsPage);
