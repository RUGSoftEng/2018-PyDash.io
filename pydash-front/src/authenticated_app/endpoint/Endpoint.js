import React, { Component } from 'react';

class Endpoint extends Component {
  

  render() {
    if(this.props.endpointData!=null){
      return (
        <h1>Page of endpoint {this.props.endpointData.name}</h1>
       
      )
    } else {
      return (
        <h1>Endpoint not found</h1>
      )
    }
    }
  }
  
  export default Endpoint;