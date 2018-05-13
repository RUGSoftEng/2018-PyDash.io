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
import {dict_to_xy_arr} from "../../../utils";

class UniqueVisitsFetcher extends StatisticFetcher {
    statistic_name = "unique_visitors_per_day";

    render = () => {
        console.log("statistic data:", this.state.statistic_data);
        if(this.state.loading){
            return (<em>Loading...</em>);
        }
        return (
            <VisitsGraph data={this.state.statistic_data[this.state.timeslice] || []} title="Unique visitors per" tooltip_title="No. unique visits: " height={400} timeslice={this.state.timeslice} />
        )
    }
}

UniqueVisitsFetcher.propTypes = {
    timeslice: PropTypes.string,
}




function UniqueVisitorsPanel(props) {
        return (
            <ExpansionPanel>
                <ExpansionPanelSummary expandIcon={<ExpandMoreIcon />}>
                    <h3>Unique Visitors Per Day</h3>
                </ExpansionPanelSummary>
                <ExpansionPanelDetails>
                    <TimesliceTabs>
                        <UniqueVisitsFetcher dashboard_id={props.dashboard_id}/>
                    </TimesliceTabs>
                </ExpansionPanelDetails>
            </ExpansionPanel>
        )
}

UniqueVisitorsPanel.propTypes = {
    dashboard_id: PropTypes.string.isRequired,
};

export default UniqueVisitorsPanel;
