import React, { Component } from 'react';
import GraphGrid from './GraphGrid';
import axios from 'axios';


class Board extends Component {
    constructor(props) {
        super(props);
        this.state = {
            dashboard: null,
        };
    }

    componentDidMount() {
      axios(window.api_path + '/api/dashboards/' + this.props.id, {
        method: 'get',
        withCredentials: true
      }).then((response) => {

        this.setState(prevState => {
            return {...prevState, dashboard: response.data}
        });
      }).catch((error) => {
        console.log('error while fetching dashboard information', error);
      });
    }

    render() {
        if(this.state.dashboard === null) {
            return (<h2>Loading...</h2>);
        }
        return (
            <div>
                <h2>Dashboard: {this.state.dashboard.url}</h2>
                <GraphGrid id={this.props.id} />
            </div>
        );
    }
}

export default Board;
