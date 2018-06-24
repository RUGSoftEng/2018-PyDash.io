import React, { Component } from 'react';

import axios from 'axios';

import _find from 'lodash-es/find';

import BoxplotPanel from './BoxplotPanel';
import MiscDataPanel from './MiscDataPanel';

class Endpoint extends Component {
  constructor(props) {
    super(props);
    this.state = {
      endpointData: {},
    };
  }

  componentDidMount() {
    axios(window.api_path + '/api/dashboards/' + this.props.dashboard_id, {
        method: 'get',
        withCredentials: true
    }).then((response) => {
        console.log("Returned data", response);
        this.setState(prevState => {
            return {
                ...prevState,
                endpointData: _find(response.data.endpoints, (endpoint) => (endpoint.name === this.props.endpointData.name)),
            }
        });
    }).catch((error) => {
        console.log('error while fetching dashboard information', error);
    });
  }

  render() {
      console.log("ENDPOINT DATA", this.state);
      if (!this.state.endpointData.aggregates) {
        return (<h2>Loading...</h2>);
      } else {
        return (
          <div>
            <h1>Page of endpoint "{this.props.endpointData.name}"</h1>
            <BoxplotPanel data={this.state.endpointData.aggregates} />
            <MiscDataPanel data={this.state.endpointData.aggregates} />
          </div>
        );
      }
    }
  }
  
  export default Endpoint;
