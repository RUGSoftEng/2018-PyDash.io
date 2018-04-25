import React from 'react';
import PropTypes from 'prop-types';
import { withStyles } from 'material-ui/styles';
import classnames from 'classnames';
import Card, { CardHeader, CardMedia, CardContent, CardActions } from 'material-ui/Card';
import Collapse from 'material-ui/transitions/Collapse';
import Avatar from 'material-ui/Avatar';
import IconButton from 'material-ui/IconButton';
import Typography from 'material-ui/Typography';
import grey from 'material-ui/colors/grey';
import FavoriteIcon from 'material-ui-icons/Favorite';
import ShareIcon from 'material-ui-icons/Share';
import BuildIcon from 'material-ui-icons/Build';
import MoreVertIcon from 'material-ui-icons/MoreVert';
import Logo from '../../images/favicon.jpg'
import graph from '../../images/line_graph.png'
const styles = theme => ({
  card: {
    
  },
  media: {
    height: 0,
    paddingTop: '56.25%', // 16:9
  },
  actions: {
    display: 'flex',
  },
  expand: {
    transform: 'rotate(0deg)',
    transition: theme.transitions.create('transform', {
      duration: theme.transitions.duration.shortest,
    }),
    marginLeft: 'auto',
  },
  expandOpen: {
    transform: 'rotate(-90deg)',
  },
  avatar: {
    backgroundColor: grey[100],
  },
});

class RecipeReviewCard extends React.Component {


  render() {
    const { classes } = this.props;

    return (
      <div>
        <Card className={classes.card}>
          <CardHeader
            avatar={
              <Avatar aria-label="Pydash" img src={Logo} className={classes.avatar}>
                
              </Avatar>
            }
            action={
            <CardActions className={classes.actions}>
            <IconButton href = {'settings'}>
              <BuildIcon />
            </IconButton>
          </CardActions>
            }
            title="Pydash card"
          />
       <CardMedia
          className={classes.media}
          image={graph}
        />
          <CardContent>
            <Typography component="p">
                This is a graph
            </Typography>
          </CardContent>

        </Card>
      </div>
    );
  }
}

RecipeReviewCard.propTypes = {
  classes: PropTypes.object.isRequired,
};

export default withStyles(styles)(RecipeReviewCard);