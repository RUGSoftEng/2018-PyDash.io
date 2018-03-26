import React from 'react';
import { ListItem, ListItemIcon, ListItemText } from 'material-ui/List';
import DonutSmall from 'material-ui-icons/DonutSmall';
import StarIcon from 'material-ui-icons/Star';
import Logout from '../logout/Logout'

export const mailFolderListItems = (
    <div>
        <ListItem button>
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