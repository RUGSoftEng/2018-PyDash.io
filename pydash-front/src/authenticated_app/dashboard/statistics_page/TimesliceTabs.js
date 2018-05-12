import React, { Component } from 'react';
import PropTypes from 'prop-types';

import AppBar from 'material-ui/AppBar';
import Tabs, { Tab } from 'material-ui/Tabs';

function TabContainer(props) {
    return (
        <div style={{ padding: 8 * 3 }}>
        {props.children}
        </div>
    );
}

TabContainer.propTypes = {
    children: PropTypes.node.isRequired,
};

class TimesliceTabs extends Component {
    constructor(props) {
        super(props);
        this.state = {
            timeslice: "day",
        }
    }

    changeTab = (_event, timeslice) => {
        this.setState({timeslice: timeslice})
    }

    render = () => {
        let updatedChildren = React.Children.map(
            this.props.children,
            (child) => (
                React.cloneElement(child, { timeslice: this.state.timeslice })
            )
        );
        return (
            <div ref={this.setElement} style={{width: "100%", overflow: 'hidden'}}>
                <AppBar position="static">
                <Tabs value={this.state.timeslice} onChange={this.changeTab}>
                    <Tab label="hour" value="hour" />
                    <Tab label="day" value="day" />
                    <Tab label="week" value="week" />
                    <Tab label="month" value="month" />
                    <Tab label="year" value="year" />
                    <Tab label="all time" value="all_time" />
                </Tabs>
            </AppBar>
            <TabContainer>
                {updatedChildren}
            </TabContainer>
            </div>
        );
    }
}

TimesliceTabs.propTypes = {
    children: PropTypes.arrayOf(PropTypes.element).isRequired,
};

export default TimesliceTabs;
