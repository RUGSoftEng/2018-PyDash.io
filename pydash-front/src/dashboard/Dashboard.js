import React, { Component } from 'react';
import './Dashboard.css';
import { withStyles } from 'material-ui/styles';
import AppBar from 'material-ui/AppBar';
import Toolbar from 'material-ui/Toolbar';
import Typography from 'material-ui/Typography';
import Button from 'material-ui/Button';
import IconButton from 'material-ui/IconButton';
import MenuIcon from 'material-ui-icons/Menu';
import ResponsiveDrawer from './ResponsiveDrawer';

const styles = {
    root: {
        flexGrow: 1,
    },
    flex: {
        flex: 1,
    },
    menuButton: {
        marginLeft: -12,
        marginRight: 20,
    },
};

class Dashboard extends Component {
    render() {
        return (
            <ResponsiveDrawer />
            // <div className="root">
            //     <AppBar position="static">
            //         <Toolbar>
            //         <IconButton className="menuButton" color="inherit" aria-label="Menu">
            //             <MenuIcon />
            //         </IconButton>
            //         <Typography variant="title" color="inherit" className="flex">
            //             Title
            //         </Typography>
            //         <Button color="inherit">Login</Button>
            //         </Toolbar>
            //     </AppBar>
            // </div>
        );
    }
}

export default withStyles(styles)(Dashboard);
