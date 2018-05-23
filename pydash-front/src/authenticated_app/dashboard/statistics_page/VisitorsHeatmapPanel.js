import React, { Component } from "react";
import PropTypes from 'prop-types';

import axios from 'axios';

// Visual:
import ExpansionPanel, {
    ExpansionPanelSummary,
    ExpansionPanelDetails,
} from 'material-ui/ExpansionPanel';
import ExpandMoreIcon from '@material-ui/icons/ExpandMore';


class VisitorsHeatmapPanel extends Component {
    constructor(props) {
        super(props);
        this.state = {
            
        }
    }

    componentDidMount() {
        // TODO Once back-end has proper API endpoints, use that one instead of the overall one.
        let start_date = '2018-05-08';
        axios.get(window.api_path + '/api/dashboards/' + this.props.dashboard_id + '/visitor_heatmap?start_date='+start_date,
            {withCredentials: true}
        ).then((response) => {
            console.log(response);
            this.setState(prevState => {
                return {
                    ...prevState,
                    
                }
            });
        }).catch((error) => {
            console.log('error while fetching heatmap information', error);
        });
    }

    render = () => {
        return (
            <ExpansionPanel>
                <ExpansionPanelSummary expandIcon={<ExpandMoreIcon />}>
                    <h3>Visitors</h3>
                </ExpansionPanelSummary>
                <ExpansionPanelDetails>
                    
                </ExpansionPanelDetails>
            </ExpansionPanel>
        );

    }
}

VisitorsHeatmapPanel.propTypes = {
    dashboard_id: PropTypes.string.isRequired,
}

export default VisitorsHeatmapPanel;
