import React from 'react';
import { Route } from 'react-router-dom';

// Visual:
import { Breadcrumb } from '@pydash/react-breadcrumbs';

const BreadcrumbRoute = ({
	  component: Component,
	  includeSearch = false,
    isLink = true,
	  render,
	  ...props
}) => (
    <Route { ...props } render={ routeProps => (
        console.log("ROUTE PROPS", routeProps.match.url),
        <Breadcrumb data={{
    	      title: props.title,
    	      pathname: routeProps.match.url,
    	      search: includeSearch ? routeProps.location.search : null,
            isLink: isLink && routeProps.match.url !== window.location.pathname,
        }}>
    	      { Component ? <Component { ...routeProps } /> : render(routeProps) }
        </Breadcrumb>
    )} />
)

export default BreadcrumbRoute;
