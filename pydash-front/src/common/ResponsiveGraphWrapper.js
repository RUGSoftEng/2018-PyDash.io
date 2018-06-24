import React, { Component } from 'react';
import PropTypes from 'prop-types';

import ContainerDimensions from 'react-container-dimensions';

/**
 * 
 * 
 */
class ResponsiveGraphWrapper extends Component {
    static propTypes = {
        height: PropTypes.number.isRequired
    }

    updatedChildren = (width) => {
        return React.Children.map(
            this.props.children,
            (child) => (
                React.cloneElement(child, { width: width })
            )
        );
    }

    render = () => (
        <div style={{width: "100%", height: this.props.height, overflow: "hidden"}}>
            <ContainerDimensions>
                {({width}) => (
                    <div style={{position: "absolute", left: 0, right: 0, top: 0, bottom: 0}}>
                        {this.updatedChildren(width)}
                    </div>
                )}
            </ContainerDimensions>
        </div>
    )
}

export default ResponsiveGraphWrapper;
