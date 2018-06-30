import React, { Component } from "react";
import PropTypes from 'prop-types';

import axios from 'axios';

// Visual:
import ExpansionPanel, {
    ExpansionPanelSummary,
    ExpansionPanelDetails,
} from 'material-ui/ExpansionPanel';
import ExpandMoreIcon from '@material-ui/icons/ExpandMore';

import VisitorsHeatmapGraph from './VisitorsHeatmapGraph';

import { getIsoDateString, convertHeatmapData } from '../../../utils';

/**
 * Panel containing a heatmap of all unique visitors that have been visiting this Dashboard.
 */
class UniqueVisitorsHeatmapPanel extends Component {
    constructor(props) {
        super(props);
        this.state = {
            heatmap: [],
        }
    }

    componentDidMount() {
        let start_date = new Date();
        start_date.setDate(start_date.getDate() - 7);
        let start_date_string = getIsoDateString(start_date);
        axios.get(window.api_path + '/api/dashboards/' + this.props.dashboard_id + '/unique_visitor_heatmap?start_date='+start_date_string,
            {withCredentials: true}
        ).then((response) => {
            let heatmapData = convertHeatmapData(response.data);
            this.setState(prevState => {
                return {
                    ...prevState,
                    heatmap: heatmapData,
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
                    <h3>Unique visitors (heatmap)</h3>
                </ExpansionPanelSummary>
                <ExpansionPanelDetails>
                    <VisitorsHeatmapGraph data={this.state.heatmap} height={200+(this.state.heatmap.length*42)} title="Unique visitors (heatmap)" />
                </ExpansionPanelDetails>
            </ExpansionPanel>
        );

    }
}

UniqueVisitorsHeatmapPanel.propTypes = {
    dashboard_id: PropTypes.string.isRequired,
}

export default UniqueVisitorsHeatmapPanel;
