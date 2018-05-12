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
        console.log("Changing tab to:", timeslice);
        this.setState({timeslice: timeslice})
    }

    render = () => {
        let children = this.props.children
        let updatedChildren;
        if(typeof(children) === 'object' ){
            children = [children]
        }
        updatedChildren = React.Children.map(
            children,
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
    children: PropTypes.objectOf(PropTypes.element).isRequired,
};

export default TimesliceTabs;
