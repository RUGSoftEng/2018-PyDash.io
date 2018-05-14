import React, { Component} from 'react';

import { TableHead, Table, TableBody, TableRow, TableCell, TableRowColumn } from "material-ui";
import Button from 'material-ui/Button';
import { withStyles } from 'material-ui/styles';
import { Link } from 'react-router-dom';

const WideTableCell = withStyles(theme => ({
    head: {
        colSpan: '3',
    }
}))(TableCell);



class EndpointsTable extends Component {
    render = () => {
        console.log(this.props.data);
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
                                <td><Button variant="raised" color="primary" component={Link} to={'overview/dashboards/'+this.props.dashboard_id+'/endpoints/'+endpoint.name}>Details</Button></td>
                            </tr>
                        )
                    })}
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

export default EndpointsTable;