<<<<<<< HEAD:pydash-front/src/app/settings/Settings.js
// import React, { Component } from 'react';
// import PropTypes from 'prop-types'
// import { Redirect } from 'react-router'
// import Button from 'material-ui/Button';
// import TextField from 'material-ui/TextField';
// import axios from 'axios';
// class Settings extends Component {
//   render(){
//     return (
//       <div>
//         User: { this..username }
//         </div>
//     )
//  }
// }

// export default Settings;
import React from 'react';
import PropTypes from 'prop-types';
import { withStyles } from 'material-ui/styles';
import ExpansionPanel, { ExpansionPanelDetails, ExpansionPanelSummary } from 'material-ui/ExpansionPanel';
import Typography from 'material-ui/Typography';
import ExpandMoreIcon from '@material-ui/icons/ExpandMore';


const styles = theme => ({
  root: {
    width: '100%',
  },
  heading: {
    fontSize: theme.typography.pxToRem(15),
    flexBasis: '33.33%',
    flexShrink: 0,
  },
  secondaryHeading: {
    fontSize: theme.typography.pxToRem(15),
    color: theme.palette.text.secondary,
  },
});

class SettingsPage extends React.Component {
  state = {
    username: this.props.username
};

componentWillMount = () => {
    this.setState({
        
    })
    console.log("App state: ", this.state, this.props);
}


  handleChange = panel => (event, expanded) => {
    this.setState({
      expanded: expanded ? panel : false,
    });
  };

  render() {
    const { classes } = this.props;
    const { expanded } = this.state;

    return (
      <div className={classes.root}>
        <ExpansionPanel expanded={expanded === 'panel4'} onChange={this.handleChange('panel4')}>
          <ExpansionPanelSummary expandIcon={<ExpandMoreIcon />}>
            <Typography className={classes.heading}>Personal data</Typography>
          </ExpansionPanelSummary>
          <ExpansionPanelDetails>
              {this.state.username}
          </ExpansionPanelDetails>
        </ExpansionPanel>
        <ExpansionPanel expanded={expanded === 'panel1'} onChange={this.handleChange('panel1')}>
          <ExpansionPanelSummary expandIcon={<ExpandMoreIcon />}>
            <Typography className={classes.heading}>General settings</Typography>
            <Typography className={classes.secondaryHeading}>Test</Typography>
          </ExpansionPanelSummary>
          <ExpansionPanelDetails>
            <Typography>
              { this.props.username }
            </Typography>
          </ExpansionPanelDetails>
        </ExpansionPanel>
        <ExpansionPanel expanded={expanded === 'panel3'} onChange={this.handleChange('panel3')}>
          <ExpansionPanelSummary expandIcon={<ExpandMoreIcon />}>
            <Typography className={classes.heading}>Advanced settings</Typography>
            <Typography className={classes.secondaryHeading}>
              Test
            </Typography>
          </ExpansionPanelSummary>
          <ExpansionPanelDetails>
            <Typography>
              Nunc vitae orci ultricies, auctor nunc in, volutpat nisl. Integer sit amet egestas
              eros, vitae egestas augue. Duis vel est augue.
            </Typography>
          </ExpansionPanelDetails>
        </ExpansionPanel>

      </div>
    );
  }
}

SettingsPage.propTypes = {
  classes: PropTypes.object.isRequired,
};

export default withStyles(styles)(SettingsPage);
=======
import React, { Component } from 'react';


class SettingsPage extends Component {
    render() {
        return (
            <p>Nothing here yet!</p>
        );
    }
}

export default SettingsPage;
>>>>>>> development:pydash-front/src/authenticated_app/settings/SettingsPage.js
