import React from 'react';
import PropTypes from 'prop-types';

// Visual:
import { withStyles } from 'material-ui/styles';
import Drawer from 'material-ui/Drawer';
import AppBar from 'material-ui/AppBar';
import Toolbar from 'material-ui/Toolbar';
import Typography from 'material-ui/Typography';
import IconButton from 'material-ui/IconButton';
import Hidden from 'material-ui/Hidden';
import Divider from 'material-ui/Divider';
import MenuIcon from 'material-ui-icons/Menu';
import UserIcon from 'material-ui-icons/AccountCircle';
import Logo from '../../images/logo.png'
import { Link } from 'react-router-dom'

// Contents:
import { Breadcrumbs } from '@pydash/react-breadcrumbs';
import { MainMenuItems, OtherMenuItems } from './Menu';


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

/**
 * Shows the user interface for logged in users:
 *
 * - The top menu
 * - The side menu that is used for navigation (whose contents live in `Menu.js`)
 * - The `Breadcrumbs` of the currently shown page.
 *
 */
class UserInterface extends React.Component {
    state = {
        mobileOpen: false,
    };

    handleDrawerToggle = () => {
        this.setState({ mobileOpen: !this.state.mobileOpen });
    };

    render() {
        const { classes, theme } = this.props;

        const drawer = (
            <div className="sidebar">

                <div className={classes.toolbar} >

                <Link to={'/overview/settings'}>
                    <UserIcon className={classes.accounticon}  />
                    <div className={classes.accountname} >
                        {this.props.username || 'Username'}
                    </div>
                </Link>

                </div>
                <Divider />
                <MainMenuItems />
                <Divider />
                <OtherMenuItems signOutHandler={this.props.signOutHandler} />
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
                        <Link to={'/overview'}>
                            <Typography variant="title" color="inherit" noWrap>
                                <img src={Logo} alt="PyDash.io logo" style={{marginTop: "15px", marginLeft: "20px", marginBottom: "10px", maxWidth: "150px"}} />
                            </Typography>
                        </Link>
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
                <Hidden smDown implementation="css" className="menubar">
                    <Drawer
                        variant="permanent"
                        open
                        classes={{
                            paper: classes.drawerPaper,
                        }}
                        className="menubar_inner"
                    >
                        {drawer}
                    </Drawer>
                </Hidden>
                <main className={classes.content}>
                    <div className={classes.toolbar} />
                    <Breadcrumbs hidden={false} separator="/" />
                    {this.props.children}
                </main>
            </div>
        );
    }
}

UserInterface.propTypes = {
    classes: PropTypes.object.isRequired,
    theme: PropTypes.object.isRequired,
};

export default withStyles(styles, { withTheme: true })(UserInterface);
