import React, { Component } from 'react';


/**
 * The `EndpointPage` renders the details page of a single EndpointPage.
 */
class EndpointPage extends Component {

  render() {
      return (
        <h1>Page of endpoint {this.props.endpointData.name}</h1>
       
      )
    }
  }
  
  export default EndpointPage;
