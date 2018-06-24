
import React, { Component } from 'react';

/**
 * This component becomes as large as its container, and then passes its resulting `width` on as the `with` prop to its child,
 * as to make child components that require a width in pixels responsive.
 *
 */
class WidthAwareContainer extends Component {
    state = {
        width: 0,
    }
    dom_element = null;

    setElement = (dom_element) => {
        this.dom_element = dom_element;
        this.updateWidth();
    }

    updateWidth = () => {
        if(this.dom_element === null){
            return
        }
        this.setState({width: this.dom_element.clientWidth});
    }

    componentDidMount = () => {
        window.addEventListener("resize", this.updateWidth);
    }

    componentWillUnmount = () => {
        window.removeEventListener("resize", this.updateWidth);
    }

    render = () => {
        let updatedChildren = React.Children.map(
            this.props.children,
            (child) => (
                React.cloneElement(child, { containerWidth: this.state.width })
            )
        );
        return (
            <div ref={this.setElement} style={{width: "100%", overflow: 'hidden'}}>
                {updatedChildren}
            </div>
        );
    }
}

export default WidthAwareContainer;
