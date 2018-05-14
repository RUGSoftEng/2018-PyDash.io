import React, { Component} from 'react';

import { TableHead, Table, TableBody, TableRow, TableCell, TableRowColumn } from "material-ui";
import { withStyles } from 'material-ui/styles';

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
                        <th rowspan="2">Endpoint</th>
                        <th colspan="3">Number of hits</th>
                        <th colspan="3">Median execution time</th>
                        <th rowspan="2">Last accessed</th>
                        <th rowspan="2">Details</th>
                    </tr>
                    <tr>
                        <th>Today</th>
                        <th>Last 7 days</th>
                        <th>Overall</th>
                        <th>Today</th>
                        <th>Last 7 days</th>
                        <th>Overall</th>
                    </tr>
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