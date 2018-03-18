import React, {Component} from 'react';
import './overview.css';
import Grid from 'material-ui/Grid';
import Card, { CardActions, CardContent } from 'material-ui/Card';
import { withStyles } from 'material-ui/styles';

const styles = {
    card: {
        minWidth: 100,
        minHeight: 100,
        'background-color': '#3f51b5',
    }
};

class DashTile extends Component {
    constructor(props) {
        super(props);
        this.state = {
            title: props.title,
        };
    }
    
    render() {
        return(
            <Grid item xs={2}>
                <Card>
                    <CardContent>
                        {this.state.title}
                    </CardContent>
                </Card>
            </Grid>
        );
    }
}

export default withStyles(styles)(DashTile);