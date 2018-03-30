import React from 'react';
import { NavLink } from 'react-router-dom'

import { ListItem, ListItemIcon, ListItemText } from 'material-ui/List';
import DonutSmall from 'material-ui-icons/DonutSmall';
import HomeIcon from 'material-ui-icons/Home';
import StarIcon from 'material-ui-icons/Star';

import Logout from './Logout'

export const mailFolderListItems = (
    <div>
        <ListItem button component={NavLink} to={'/dashboard/'}>
            <ListItemIcon>
                <HomeIcon />
            </ListItemIcon>
            <ListItemText primary="Overview" />
        </ListItem>
        <ListItem button component={NavLink} to={'/dashboard/statistics'}>
            <ListItemIcon>
                <DonutSmall />
            </ListItemIcon>
            <ListItemText primary="Statistics" />
        </ListItem>
        <ListItem button>
            <ListItemIcon>
                <StarIcon />
            </ListItemIcon>
            <ListItemText primary="Analytics" />
        </ListItem>
    </div>
);

export const otherMailFolderListItems = (
    <div>
        <Logout />
    </div>
);