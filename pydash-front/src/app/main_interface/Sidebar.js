import React from 'react';
import { NavLink } from 'react-router-dom'

import { ListItem, ListItemIcon, ListItemText } from 'material-ui/List';
import SettingsIcon from 'material-ui-icons/Settings';
import HomeIcon from 'material-ui-icons/Home';
import BuildIcon from 'material-ui-icons/Build'


import Logout from './Logout'


import {Howl} from 'howler';
import menu_soundfile from './woosh.mp3';
const menu_sound = new Howl({
    src: [menu_soundfile],
    volume: 0.8
});

function playMenuSound(){
    menu_sound.play();
}


export const mailFolderListItems = (props) => {
    return (
        <div>
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

        <ListItem button component={NavLink} to={'/dashboard/TestCards'}>
            <ListItemIcon>
                <BuildIcon />
            </ListItemIcon>
            <ListItemText primary="Test Cards" />
        </ListItem>
        </div>
    );
}


export const otherMailFolderListItems = (props) => {
    return (
        <div>
            <Logout signOutHandler={props.signOutHandler}/>
        </div>
    );
}
