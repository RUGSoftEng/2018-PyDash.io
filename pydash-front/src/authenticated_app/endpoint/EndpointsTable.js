import React, { Component} from 'react';


import Button from 'material-ui/Button';
import { Link } from 'react-router-dom';
import TextField from 'material-ui/TextField';

import {withRouter} from "react-router-dom";

let endpoint_url = (dashboard_id, endpoint_name) => ('/overview/dashboards/'+dashboard_id+'/endpoints/'+endpoint_name);

class EndpointsTable extends Component {
    state = {
        input:'',
    };

    handleType = key => event => {
        this.setState({
            [key]: event.target.value
        });
      };

    render = () => {
        console.log("ENDPOINTS TABLE", this.props.data);
        if(this.props.data.length === 0) {
            return (
                <em>
                    No Endpoints could currently be found for this Dashboard.
                </em>
            )
        }

        return (

            <div className="EndpointsTable" >
                <TextField
                id="filter"
                label="Filter endpoints"
                value={this.state.input}
                onChange={this.handleType('input')}
                margin="normal"
                />
                <table width="100%">
                    <thead>
                    <tr>
                        <th></th>
                        <th colSpan="2">Number of hits</th>
                        <th colSpan="2">Execution times</th>
                        <th></th>
                        <th></th>
                    </tr>
                    <tr>
                        <th>Endpoint</th>
                        <th>Unique</th>
                        <th>Total</th>
                        <th>Average</th>
                        <th>Total</th>
                        <th>Details</th>
                    </tr>
                    </thead>
                    {this.props.data.map((endpoint) => {
                        if(this.state.input === '' || endpoint.name.includes(this.state.input)){
                            let endpoint_link = endpoint_url(this.props.dashboard_id, endpoint.name);
                            return (
                                <tr>
                                    <td><a href={endpoint_link} onClick={(e) => {e.preventDefault(); this.props.history.push(endpoint_link)}} >{endpoint.name}</a></td>
                                    <td>{endpoint.aggregates.unique_visitors}</td>
                                    <td>{endpoint.aggregates.total_visits}</td>
                                    <td>{endpoint.aggregates.average_execution_time}</td>
                                    <td>{endpoint.aggregates.total_execution_time}</td>
                                    <td><Button variant="raised" color="primary" component={Link} to={endpoint_link}>Details</Button></td>
                                </tr>
                            )
                        } 
                        return console.log('none'); 

                    
                        }
                        
                    )}

                </table>
                {/*<Table>
                    <TableHead>
                        <TableRow>
                            <TableCell></TableCell>
                            <WideTableCell>Number of hits</WideTableCell>
                            <WideTableCell>Median response time</WideTableCell>
                            <TableCell></TableCell>
                            <TableCell></TableCell>
                        </TableRow>
                        <TableRow>
                            <TableCell>Endpoint</TableCell>
                            <TableCell>Today</TableCell>
                            <TableCell>Last 7 days</TableCell>
                            <TableCell>Overall</TableCell>
                            <TableCell>Today</TableCell>
                            <TableCell>Last 7 days</TableCell>
                            <TableCell>Overall</TableCell>
                            <TableCell>Last accessed</TableCell>
                            <TableCell>Details</TableCell>
                        </TableRow>
                    </TableHead>
                    <TableBody>
                                                
                    </TableBody>
                </Table>*/}
            </div>
        );
    }
}

export default withRouter(EndpointsTable);
