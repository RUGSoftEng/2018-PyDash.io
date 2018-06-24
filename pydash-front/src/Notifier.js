import React from 'react';
import Snackbar from 'material-ui/Snackbar';

let openSnackbarFunction;

/**
 * This component shows the notifications ('Snackbars') that the app might generate.
 * This has been put in its own component that is included at the outside of the application,
 * so that logging in/logging out and other state changes that might completely alter how the page will look,
 * will be able to show notifications as well.
 *
 * The Notifier component is not used directly from within the app. Rather, the `showNotification()` function that this component file exports is.
 * The application should only contain one Notifier component, because the `showNotification()` function expects there to only be one Notifier.
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
