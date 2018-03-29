import React, {Component} from 'react';
import './overview.css';
import Grid from 'material-ui/Grid';
import Card, { CardContent } from 'material-ui/Card';
import { withStyles } from 'material-ui/styles';
import Typography from 'material-ui/Typography';

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
            col: props.xs,
        };
    }
    
    render() {
        return(
            <Grid item xs={this.state.col}>
                <Card>
                    <CardContent>
                        <Typography variant='headline' component='h2'>
                            {this.state.title}
                        </Typography>
                    </CardContent>
                </Card>
            </Grid>
        );
    }
}

export default withStyles(styles)(DashTile);
