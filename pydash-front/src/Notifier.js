import React from 'react';
import Snackbar from 'material-ui/Snackbar';

let openSnackbarFunction;

class Notifier extends React.Component {
  state = {
    open: false,
    message: '',
  };

  componentDidMount() {
    openSnackbarFunction = this.openSnackbar;
  }

  openSnackbar = ({ message }) => {
    this.setState({
      open: true,
      message,
    });
  };

  handleSnackbarClose = () => {
    this.setState({
      open: false,
      message: '',
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
        autoHideDuration={5000}
        onClose={this.handleSnackbarClose}
        open={this.state.open}
      />
    );
  }
}

export function showNotification({ message }) {
  openSnackbarFunction({ message });
}

export default Notifier;
