import React from 'react';

// Routing:
import { NavLink } from 'react-router-dom'

// Visual:
import List, { ListItem, ListItemIcon, ListItemText } from 'material-ui/List';
import SettingsIcon from 'material-ui-icons/Settings';
import HomeIcon from 'material-ui-icons/Home';

// Contents:
import Logout from './Logout'

// Sound:
import {Howl} from 'howler';
import menu_soundfile from './woosh.mp3';


const menu_sound = new Howl({
    src: [menu_soundfile],
    volume: 0.8
});

function playMenuSound(){
    menu_sound.play();
}

export const MainMenuItems = (props) => {
    return (
        <List>
            <ListItem button component={NavLink} to={'/dashboard/'} onClick={playMenuSound}>
                <ListItemIcon>
                    <HomeIcon />
                </ListItemIcon>
                <ListItemText primary="Dashboards" />
            </ListItem>
            <ListItem button component={NavLink} to={'/dashboard/settings'} onClick={playMenuSound}>
                <ListItemIcon>
                    <SettingsIcon />
                </ListItemIcon>
                <ListItemText primary="Settings" />
            </ListItem>
        </List>
    );
}

export const OtherMenuItems = (props) => {
    return (
        <List>
            <Logout signOutHandler={props.signOutHandler}/>
        </List>
    );
}
