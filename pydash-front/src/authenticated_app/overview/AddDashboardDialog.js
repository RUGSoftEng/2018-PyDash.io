import React, { Component } from 'react';
import Button from 'material-ui/Button';
import TextField from 'material-ui/TextField';
import Dialog, {
    DialogActions,
    DialogContent,
    DialogContentText,
    DialogTitle,
} from 'material-ui/Dialog';

class AddDashboardDialog extends Component {
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
                            label="Dashboard URL"
                            type="url"
                            fullWidth
                            required
                        />
                        <TextField
                            id="name"
                            label="Dashboard name"
                            type="text"
                            fullWidth 
                        />
                        <TextField 
                            id="code"
                            label="Security code"
                            type="password"
                            fullWidth 
                            required
                        />
                    </DialogContent>
                    <DialogActions>
                        <Button onClick={this.props.onClose} color="#fff">
                            Cancel
                        </Button>
                        <Button onClick={this.props.onClose} color="primary">
                            Save
                        </Button>
                    </DialogActions>
                </Dialog>
            </div>
        );
    }

}

export default AddDashboardDialog;