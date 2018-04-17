import React, { Component } from 'react';
import GraphGrid from './GraphGrid';



class Board extends Component {
    render() {
        return (
            <GraphGrid id={this.props.id} />
        );
    }
}

export default Board;
