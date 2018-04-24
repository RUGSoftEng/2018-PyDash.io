import React from 'react';
import { Route } from 'react-router-dom'
import PropTypes from 'prop-types';

// material-ui
import { withStyles } from 'material-ui/styles';
import Drawer from 'material-ui/Drawer';
import AppBar from 'material-ui/AppBar';
import Toolbar from 'material-ui/Toolbar';
import List from 'material-ui/List';
import Typography from 'material-ui/Typography';
import IconButton from 'material-ui/IconButton';
import Hidden from 'material-ui/Hidden';
import Divider from 'material-ui/Divider';
import MenuIcon from 'material-ui-icons/Menu';
import UserIcon from 'material-ui-icons/AccountCircle';

// APP
import { mailFolderListItems, otherMailFolderListItems } from './Sidebar';
import Overview from '../overview/Overview';
import Statistics from '../statistics/Statistics';
import Board from '../boards/Board';
import Settings from '../settings/Settings';
import TestCards from '../testingCards/TestCards'


// Styling
import Logo from '../../images/logo.png'

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
    accounticon: {
        position: 'absolute',
        top: 17,
        left: 30,
        fontSize: 36,
        color: 'rgba(0, 0, 0, 0.54)'
    },
    accountname: {
        position: 'absolute',
        top: 25,
        left: 80,
        color: 'rgba(0, 0, 0, 0.54)'
    },
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

class ResponsiveDrawer extends React.Component {
    state = {
        mobileOpen: false,
    };

    handleDrawerToggle = () => {
        this.setState({ mobileOpen: !this.state.mobileOpen });
    };

    render() {
        const { classes, theme } = this.props;

        const drawer = (
            <div>

                <div className={classes.toolbar}>
                    <UserIcon className={classes.accounticon} />
                    <div className={classes.accountname}>
                        {this.props.username || 'Username'}
                    </div>
                </div>
                <Divider />
                <List>{mailFolderListItems}</List>
                <Divider />
                <List>{otherMailFolderListItems}</List>
            </div>
        );

        return (
            <div className={classes.root}>
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
                            <img src={Logo} alt="PyDash.io logo" style={{marginTop: "15px", marginLeft: "20px", marginBottom: "10px", maxWidth: "150px"}} />
            </Typography>
                    </Toolbar>
                </AppBar>
                <Hidden mdUp>
                    <Drawer
                        variant="temporary"
                        anchor={theme.direction === 'rtl' ? 'right' : 'left'}
                        open={this.state.mobileOpen}
                        onClose={this.handleDrawerToggle}
                        classes={{
                            paper: classes.drawerPaper,
                        }}
                        ModalProps={{
                            keepMounted: true, // Better open performance on mobile.
                        }}
                    >
                        {drawer}
                    </Drawer>
                </Hidden>
                <Hidden smDown implementation="css">
                    <Drawer
                        variant="permanent"
                        open
                        classes={{
                            paper: classes.drawerPaper,
                        }}
                    >
                        {drawer}
                    </Drawer>
                </Hidden>
                <main className={classes.content}>
                    <div className={classes.toolbar} />
                    <Route exact path='/dashboard' component={Overview} />
                    <Route exact path='/dashboard/settings' component={Settings} />
                    <Route exact path='/dashboard/statistics' component={Statistics} />
                    <Route exact path='/dashboard/TestCards' component={TestCards} />
                    <Route path='/dashboard/view/:id' component={Db} />                    
                </main>
            </div>
        );
    }

    
}

const Db = ({match}) => {
    return <Board id={match.params.id} />
}

ResponsiveDrawer.propTypes = {
    classes: PropTypes.object.isRequired,
    theme: PropTypes.object.isRequired,
};

export default withStyles(styles, { withTheme: true })(ResponsiveDrawer);
