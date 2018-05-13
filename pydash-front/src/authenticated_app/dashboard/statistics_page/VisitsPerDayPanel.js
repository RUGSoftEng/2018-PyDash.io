import React, { Component } from 'react';
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

// Utils:
import {requestStatisticData} from "./statistics_utils"


class VisitsFetcher extends StatisticFetcher {
    statistic_name = "visits_per_day";

    render = () => {
        if(this.state.loading){
            return (<em>Loading...</em>);
        }
        return (
            <VisitsGraph data={this.state.visits[this.state.timeslice]} title="Visits per" tooltip_title="No. visits: " height={400} timeslice={this.state.timeslice} />
        )
    }
}

VisitsFetcher.propTypes = {
    timeslice: PropTypes.string,
}


function VisitsPerDayPanel(props) {
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

VisitsPerDayPanel.propTypes = {
    dashboard_id: PropTypes.string.isRequired,
};

export default VisitsPerDayPanel;
