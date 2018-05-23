import React, { Component} from 'react';

import Button from 'material-ui/Button';
import { Link } from 'react-router-dom';

class EndpointsTable extends Component {
    render = () => {
        return (
            <div className="EndpointsTable">
                <table width="100%">
                    <tr>
                        <th></th>
                        <th colspan="2">Number of hits</th>
                        <th colspan="2">Execution times</th>
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
                    {this.props.data.map((endpoint) => {
                        return (
                            <tr>
                                <td>{endpoint.name}</td>
                                <td>{endpoint.aggregates.unique_visitors}</td>
                                <td>{endpoint.aggregates.total_visits}</td>
                                <td>{endpoint.aggregates.average_execution_time}</td>
                                <td>{endpoint.aggregates.total_execution_time}</td>
                                <td><Button variant="raised" color="primary" component={Link} to={'/overview/dashboards/'+this.props.dashboard_id+'/endpoints/'+endpoint.name}>Details</Button></td>
                            </tr>
                        )
                    })}
                </table>
            </div>
        );
    }
}

export default EndpointsTable;
