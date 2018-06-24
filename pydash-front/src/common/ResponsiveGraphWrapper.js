import React, { Component } from 'react';
import PropTypes from 'prop-types';

import ContainerDimensions from 'react-container-dimensions';

/**
 * A Nivo Graph component (or other component that you want to auto-resize to fill its container width), can be added to this component to ensure that this resizing will happen.
 *
 * This component will pass on the 'width' prop to the child, which will be set to the measured width the component ('s container, the ResponsiveGraphWrapper itself) currently has on the page.
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
