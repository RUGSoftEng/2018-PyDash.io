import React, { Component } from 'react';
import './overview.css';
import { withStyles } from 'material-ui/styles';
// import AppBar from 'material-ui/AppBar';
// import Toolbar from 'material-ui/Toolbar';
// import Typography from 'material-ui/Typography';
// import Button from 'material-ui/Button';
// import IconButton from 'material-ui/IconButton';
// import MenuIcon from 'material-ui-icons/Menu';
import ResponsiveDrawer from './../dashboard/ResponsiveDrawer';
import DashTileGrid from './DashTileGrid';
import AppBar from 'material-ui/AppBar';
import Toolbar from 'material-ui/Toolbar';
import MenuIcon from 'material-ui-icons/Menu';
import IconButton from 'material-ui/IconButton';
import Typography from 'material-ui/Typography';

const drawerWidth = 240;

const styles = theme => ({
    root: {
        flexGrow: 1,
        // height: 430,
        height: '100%',
        zIndex: 1,
        overflow: 'hidden',
        position: 'relative',
        display: 'flex',
        width: '100%',
    },
    appBar: {
        position: 'absolute',
        marginLeft: drawerWidth,
        [theme.breakpoints.up('md')]: {
            width: `calc(100% - ${drawerWidth}px)`,
        },
    },
    navIconHide: {
        [theme.breakpoints.up('md')]: {
            display: 'none',
        },
    },
    toolbar: theme.mixins.toolbar,
    drawerPaper: {
        width: drawerWidth,
        [theme.breakpoints.up('md')]: {
            position: 'relative',
        },
    },
    content: {
        flexGrow: 1,
        backgroundColor: theme.palette.background.default,
        padding: theme.spacing.unit * 3,
    },
});

class Overview extends Component {
    
  
    render() {
        const {classes , theme} = this.props;
        return (
          <div className = {classes.root}>
            <AppBar className={classes.appBar}>
              <Toolbar>
                <IconButton
                    color="inherit"
                    aria-label="open drawer"
                    onClick={this.handleDrawerToggle}
                    className={classes.navIconHide}
                >
                    <MenuIcon />
                </IconButton>
                <Typography variant="title" color="inherit" noWrap>
                  PyDash.io Dashboard
                </Typography>
              </Toolbar>
            </AppBar>
            <main className={classes.content}>
              <div className={classes.toolbar} />
              <DashTileGrid username='testuser' />
            </main>
          </div>
            
        );
    }
}

export default withStyles(styles)(Overview);
