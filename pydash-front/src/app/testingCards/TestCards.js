import React, { Component } from 'react';
import Card from 'material-ui/Card'
import {CardActions, CardHeader, CardMedia, CardTitle, CardText} from 'material-ui/Card';
import CreateIcon from 'material-ui-icons/Create';
import { NavLink } from 'react-router-dom'
import { ListItem, ListItemIcon, ListItemText } from 'material-ui/List';
import Grid from 'material-ui/Grid';
class TestCards extends Component {
    render() {
        return (
            <Grid>

            <Card>
              <CardActions>
              <ListItem button component={NavLink} to={'/dashboard/settings'}>
                <ListItemIcon>
                    <CreateIcon />
                </ListItemIcon>
            </ListItem>
                </CardActions>
              Hola 
              </Card>
                    
            </Grid>
        );
    }
}

export default TestCards;
