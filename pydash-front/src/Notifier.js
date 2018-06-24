import React from 'react';
import Snackbar from 'material-ui/Snackbar';

let openSnackbarFunction;
/**
 * This component ensures the snackbar notification bar functions correctly,
 *  for example by making it visible long enough to be readable 
 * 
 */
class Notifier extends React.Component {
    state = {
        open: false,
        message: '',
        preventClosing: false,
        autoHideDuration: 5000
    };

    componentDidMount() {
        openSnackbarFunction = this.openSnackbar;
    }

    openSnackbar = ({ message, autoHideDuration, preventClosing }) => {
        this.setState({
            open: true,
            message,
            autoHideDuration,
            preventClosing
        });
    };

    handleSnackbarClose = () => {
        if(this.state.preventClosing)
            return;
        this.setState({
            open: false,
            message: '',
            preventClosing: false,
            autoHideDuration: 5000,
        });
    };

    render() {
        const message = (
                <span
            id="snackbar-message-id">
                {this.state.message}
            </span>
        );

        return (
                <Snackbar
            message={message}
            autoHideDuration={ this.state.preventClosing ? null : this.state.autoHideDuration}
            onClose={this.handleSnackbarClose}
            open={this.state.open}
                />
        );
    }
}

export function showNotification({ message, autoHideDuration, preventClosing }) {
    autoHideDuration = autoHideDuration !== undefined ? autoHideDuration : 5000;
    if (preventClosing === true) {
        autoHideDuration = null;
    }
    openSnackbarFunction({ message, autoHideDuration, preventClosing });
}

export default Notifier;
