import React, { Component } from 'react';

class Endpoint extends Component {

  render() {
      return (
        <h1>Page of endpoint {this.props.endpointData.name}</h1>
       
      )
    }
  }
  
  export default Endpoint;
