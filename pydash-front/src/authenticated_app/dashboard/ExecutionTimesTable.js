import React, { Component } from "react";
import { Table, TableBody, TableRow, TableCell } from "material-ui";

import ExpansionPanel, {
    ExpansionPanelSummary,
    ExpansionPanelDetails,
} from 'material-ui/ExpansionPanel';
import ExpandMoreIcon from '@material-ui/icons/ExpandMore';
import axios from 'axios';



class ExecutionTimesTable extends Component {
    constructor(props) {
        super(props);
        this.state = {
            average_execution_time: 0,
            total_execution_time: 0,
        }
    }

    componentDidMount() {
        // TODO Once back-end has proper API endpoints, use that one instead of the overall one.
        axios(window.api_path + '/api/dashboards/' + this.props.dashboard_id, {
            method: 'get',
            withCredentials: true
        }).then((response) => {
            this.setState(prevState => {
                return {
                    ...prevState,
                    average_execution_time: response.data.aggregates.average_execution_time,
                    total_execution_time: response.data.aggregates.total_execution_time,
                }
            });
        }).catch((error) => {
            console.log('error while fetching dashboard information', error);
        });
    }

    render = () => {
        return (
            <ExpansionPanel>
                <ExpansionPanelSummary expandIcon={<ExpandMoreIcon />}>
                    <h3>Dashboard-wide execution times</h3>
                </ExpansionPanelSummary>
                <ExpansionPanelDetails>
                    <Table>
                        <TableBody>
                            <TableRow>
                                <TableCell>Average execution time</TableCell>
                                <TableCell>{this.state.average_execution_time} ms</TableCell>
                            </TableRow>
                            <TableRow>
                                <TableCell>Total execution time</TableCell>
                                <TableCell>{this.state.total_execution_time} ms</TableCell>
                            </TableRow>
                        </TableBody>
                    </Table>
                </ExpansionPanelDetails>
            </ExpansionPanel>
        );

    }
}

export default ExecutionTimesTable;