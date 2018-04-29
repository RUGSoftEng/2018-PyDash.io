import React, { Component } from 'react';
import Card from 'material-ui/Card';
import Grid from 'material-ui/Grid';
import Typography from 'material-ui/Typography';
import ExpansionPanel, {
    ExpansionPanelSummary,
    ExpansionPanelDetails,
} from 'material-ui/ExpansionPanel';
import ExpandLessIcon from '@material-ui/icons/ExpandLess';
import ExpandMoreIcon from '@material-ui/icons/ExpandMore';

class ExpandableGraphRow extends Component {
    constructor(props) {
        super(props);
        this.state = {
            expanded: false
        };
    }

    toggleExpanded = () => {
        this.setState(prevState => {
            return {...this.state, expanded: !prevState.expanded};
        });
    }

    render = () => {
        const { classes } = this.props;

        return (
            //     <Card>
            //     <h2>{this.props.title}</h2>
            //     {this.state.expanded ? <ExpandLessIcon/> : <ExpandMoreIcon/>}
            //     <div>
            //         {this.state.expanded ? this.props.children : '' }
            //     </div>
            // </Card>
            <ExpansionPanel>
                <ExpansionPanelSummary expandIcon={<ExpandMoreIcon />}>
                <h3>{this.props.title}</h3>
                </ExpansionPanelSummary>
                <ExpansionPanelDetails>
                    {this.props.children}
                </ExpansionPanelDetails>
            </ExpansionPanel>
        );
    }
}

export default ExpandableGraphRow;
