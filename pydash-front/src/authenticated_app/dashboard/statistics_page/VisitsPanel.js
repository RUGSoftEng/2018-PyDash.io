import React from 'react';
import PropTypes from 'prop-types';

import StatisticFetcher from "./StatisticFetcher"

// Visual:
import ExpansionPanel, {
    ExpansionPanelSummary,
    ExpansionPanelDetails,
} from 'material-ui/ExpansionPanel';
import ExpandMoreIcon from '@material-ui/icons/ExpandMore';

// Contents:
import TimesliceTabs from './TimesliceTabs';
import VisitsGraph from './VisitsGraph';


class VisitsFetcher extends StatisticFetcher {
    statistic_name = "total_visits";

    render = () => {
        console.log("statistic data:", this.state.statistic_data);
        if(this.state.loading){
            return (<em>Loading...</em>);
        }
        return (
            <VisitsGraph data={this.state.statistic_data[this.state.timeslice] || []} title="Visits per" tooltip_title="No. visits: " height={400} timeslice={this.state.timeslice} />
        )
    }
}

VisitsFetcher.propTypes = {
    timeslice: PropTypes.string,
}


function VisitsPanel(props) {
    return (
        <ExpansionPanel>
            <ExpansionPanelSummary expandIcon={<ExpandMoreIcon />}>
                <h3>No. Visitors</h3>
            </ExpansionPanelSummary>
            <ExpansionPanelDetails>
                <TimesliceTabs>
                    <VisitsFetcher dashboard_id={props.dashboard_id}/>
                </TimesliceTabs>
            </ExpansionPanelDetails>
        </ExpansionPanel>
    )
}

VisitsPanel.propTypes = {
    dashboard_id: PropTypes.string.isRequired,
};

export default VisitsPanel;
