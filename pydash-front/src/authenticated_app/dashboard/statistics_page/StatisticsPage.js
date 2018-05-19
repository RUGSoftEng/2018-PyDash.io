import React, { Component } from 'react';
import PropTypes from 'prop-types';

import axios from 'axios';

// Contents:
import VisitsPanel from './VisitsPanel';
import UniqueVisitorsPanel from './UniqueVisitorsPanel';
import EndpointExecutionTimesPanel from './EndpointExecutionTimesPanel';
import ExecutionTimesTable from './ExecutionTimesTable';
import EndpointsTable from '../../endpoint/EndpointsTable';

// Visual:
import { withStyles } from 'material-ui/styles';
import SwipeableViews from 'react-swipeable-views';
import Tabs, { Tab } from 'material-ui/Tabs';
import Typography from 'material-ui/Typography';

// Helper:
import {dict_to_xy_arr} from "../../../utils";


function TabContainer({ children, dir }) {
  return (
    <Typography component="div" dir={dir} style={{ padding: 8 * 3 }}>
      {children}
    </Typography>
  );
}

TabContainer.propTypes = {
  children: PropTypes.node.isRequired,
  dir: PropTypes.string.isRequired,
};

const styles = theme => ({
  root: {
    backgroundColor: theme.palette.background.paper,
    width: 500,
  },
});


class StatisticsPage extends Component {
    constructor(props) {
        super(props);
        this.divRef = React.createRef();
        this.state = {
            dashboard: null,
            visits_per_day: [],
            unique_visitors_per_day: [],
            average_execution_times: [],
            error: "",
            width: 0,
            current_tab: 0,
        };
    }

    componentDidMount() {
        console.log(this.divRef);
        
        this.setState(prevState => {
            /* const width =  this.divRef.current.clientWidth;*/
            const width = window.screen.width;
            return {...prevState, width: width}
        })

        axios(window.api_path + '/api/dashboards/' + this.props.dashboard.id, {
            method: 'get',
            withCredentials: true
        }).then((response) => {
            //console.log(response);
            if (response.data.hasOwnProperty('error')) {
                this.setState(prevState => {
                    return {
                        ...prevState,

                        dashboard: response.data,
                        

                        total_visits: response.data.aggregates.total_visits,
                        visits_per_day: dict_to_xy_arr(response.data.aggregates.visits_per_day),
                        unique_visitors_per_day: dict_to_xy_arr(response.data.aggregates.unique_visitors_per_day),
                        error: response.data.error,
                    }
                });
            } else {
                this.setState(prevState => {
                    return {
                        ...prevState,


                        dashboard: response.data,

                        total_visits: response.data.aggregates.total_visits,
                        visits_per_day: dict_to_xy_arr(response.data.aggregates.visits_per_day),
                        unique_visitors_per_day: dict_to_xy_arr(response.data.aggregates.unique_visitors_per_day),
                    };
                });
            }
        }).catch((error) => {
            console.log('error while fetching dashboard information', error);
        });
    }

    /* handleChange = (event, value) => {
     *     this.setState({ value });
     *   }; */
    changeTab = (event, value) => {
        this.setState({current_tab: value})
    }
    
    handleChangeIndex = index => {
        this.setState({ value: index });
    };

    render() {
        const { theme } = this.props;
        if(this.props.dashboard === null || this.state.dashboard === null) {
            return (<h2>Loading...</h2>);
        }
        
        return (
            

            <div className={"Name"}>
              <Tabs
                value={this.state.current_tab}
                onChange={this.changeTab}
                indicatorColor="primary"
                textColor="primary"
                centered
              >
                <Tab label="Statistics" />
                <Tab label="Endpoints" />
                <Tab label="Settings" />
              </Tabs>
            <SwipeableViews
              axis={theme.direction === 'rtl' ? 'x-reverse' : 'x'}
              index={this.state.current_tab}
              onChangeIndex={this.handleChangeIndex}
            >
              <TabContainer dir={theme.direction}>
                 <div ref={this.divRef} >
                    <h2>Dashboard: {this.state.dashboard.url}</h2>
                    <h3>{this.state.error}</h3>
                    <div>
                        <VisitsPanel dashboard_id={this.props.dashboard.id} />
                        <UniqueVisitorsPanel dashboard_id={this.props.dashboard.id} />
                        <ExecutionTimesTable dashboard_id={this.props.dashboard.id} />
                        <EndpointExecutionTimesPanel dashboard_id={this.props.dashboard.id} />
                    </div>
                </div>
              </TabContainer>
              <TabContainer dir={theme.direction}>
                <div>

                    <EndpointsTable data={this.state.dashboard.endpoints} dashboard_id={this.props.dashboard.id} />
                {/*<h2>Names of endpoints:</h2>
                    <List>
                    {this.state.dashboard.endpoints.map((userData) => {
                        return (
                            <Link  to={'/overview/dashboards/'+this.props.dashboard.id+'/endpoints/'+userData.name}>
                                <ListItem>{userData.name}</ListItem>
                            </Link>
                        )
                    })}
                    </List>*/}
                    
                    
                 </div>
              </TabContainer>
              <TabContainer dir={theme.direction}>
                  <p>Nothing here yet!</p>
              </TabContainer>
            </SwipeableViews>
          </div>
        );
    }
}

StatisticsPage.propTypes = {
    theme: PropTypes.object.isRequired,
    dashboard: PropTypes.shape({
        id: PropTypes.string.isRequired,
        url: PropTypes.string.isRequired,
    }).isRequired,
};


export default withStyles(styles, { withTheme: true })(StatisticsPage);
