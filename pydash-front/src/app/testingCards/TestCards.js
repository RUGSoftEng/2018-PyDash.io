// import React, { Component } from 'react';
// import Card from 'material-ui/Card'
// import {CardActions, CardHeader, CardMedia, CardTitle, CardText} from 'material-ui/Card';
// import BuildIcon from 'material-ui-icons/Build';
// import { NavLink } from 'react-router-dom'
// import { ListItem, ListItemIcon, ListItemText } from 'material-ui/List';
// import Grid from 'material-ui/Grid';
// class TestCards extends Component {
//     render() {
//         return (
//             <Grid>

//             <Card>
//               <CardActions align="end" >
//               <ListItem  button component={NavLink} to={'/dashboard/settings'}>
//                 <ListItemIcon>
//                     <BuildIcon />
//                 </ListItemIcon>
//             </ListItem>
//                 </CardActions>
//               Hola 
//               </Card>
                    
//             </Grid>
//         );
//     }
// }

// export default TestCards;
// import React from 'react';
// import PropTypes from 'prop-types';
// import { withStyles } from 'material-ui/styles';
// import Card, { CardActions, CardContent } from 'material-ui/Card';
// import Button from 'material-ui/Button';
// import Typography from 'material-ui/Typography';

// const styles = {
//   card: {
//     minWidth: 275,
//   },
//   bullet: {
//     display: 'inline-block',
//     margin: '0 2px',
//     transform: 'scale(0.8)',
//   },
//   title: {
//     marginBottom: 16,
//     fontSize: 14,
//   },
//   pos: {
//     marginBottom: 12,
//   },
// };

// function SimpleCard(props) {
//   const { classes } = props;
//   const bull = <span className={classes.bullet}>•</span>;

//   return (
//     <div>
//       <Card className={classes.card}>
//         <CardContent>
//           <Typography className={classes.title} color="textSecondary">
//             CARD
//           </Typography>
//           <Typography variant="headline" component="h2">
//             GRAPH
//           </Typography>

//         </CardContent>

//       </Card>
//     </div>
//   );
// }

// SimpleCard.propTypes = {
//   classes: PropTypes.object.isRequired,
// };

// export default withStyles(styles)(SimpleCard);
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
    maxWidth: 400,
  },
  media: {
    height: 0,
    paddingTop: '56.25%', // 16:9
    maxWidth: 400,
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
  state = { expanded: false };

  handleExpandClick = () => {
    this.setState({ expanded: !this.state.expanded });
  };

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
            <CardActions className={classes.actions} disableActionSpacing>
            <IconButton
              className={classnames(classes.expand, {
                [classes.expandOpen]: this.state.expanded,
              })}
              onClick={this.handleExpandClick}
              aria-expanded={this.state.expanded}
              aria-label="Dashboard Settings"
            >
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
          
          <Collapse in={this.state.expanded} timeout="auto" unmountOnExit>
            <CardContent>
            <Typography component="p">
                These are the settings for the graph
            </Typography>
            </CardContent>
          </Collapse>
        </Card>
      </div>
    );
  }
}

RecipeReviewCard.propTypes = {
  classes: PropTypes.object.isRequired,
};

export default withStyles(styles)(RecipeReviewCard);