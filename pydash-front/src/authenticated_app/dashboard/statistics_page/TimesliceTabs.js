import React, { Component } from 'react';
import PropTypes from 'prop-types';

// Visual:
import Tabs, { Tab } from 'material-ui/Tabs';

/**
 * Container that the `TimesliceTabs` will fill with children that receive the extra 'timeslice' prop.
 */
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

/**
 * A component put inside this component will receive the `timeslice` property
 *
 * This property is set, depending on the tab that the user selects (one of hour, day, week, month, year)
 */
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
            <div style={{width: "100%"}}>
                <Tabs value={this.state.timeslice} onChange={this.changeTab} centered>
                    <Tab label="hour" value="hour" />
                    <Tab label="day" value="day" />
                    <Tab label="week" value="week" />
                    <Tab label="month" value="month" />
                    <Tab label="year" value="year" />
                </Tabs>
            <TabContainer>
                {updatedChildren}
            </TabContainer>
            </div>
        );
    }
}

export default TimesliceTabs;
