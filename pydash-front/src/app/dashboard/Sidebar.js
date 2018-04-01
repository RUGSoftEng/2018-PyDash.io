import React from 'react';
import { NavLink } from 'react-router-dom'

import { ListItem, ListItemIcon, ListItemText } from 'material-ui/List';
import DonutSmall from 'material-ui-icons/DonutSmall';
import SettingsIcon from 'material-ui-icons/Settings';
import HomeIcon from 'material-ui-icons/Home';
import StarIcon from 'material-ui-icons/Star';

import Logout from './Logout'

export const mailFolderListItems = (
    <div>
        <ListItem button component={NavLink} to={'/dashboard/'}>
            <ListItemIcon>
                <HomeIcon />
            </ListItemIcon>
            <ListItemText primary="Dashboards" />
        </ListItem>
        <ListItem button component={NavLink} to={'/dashboard/statistics'}>
            <ListItemIcon>
                <SettingsIcon />
            </ListItemIcon>
            <ListItemText primary="Settings" />
        </ListItem>
    </div>
);

export const otherMailFolderListItems = (
    <div>
        <Logout />
    </div>
);
