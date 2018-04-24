import React, { Component } from 'react';
import Card from 'material-ui/Card'
import {CardActions, CardHeader, CardMedia, CardTitle, CardText} from 'material-ui/Card';
import BuildIcon from 'material-ui-icons/Build';
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
                    <BuildIcon />
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
