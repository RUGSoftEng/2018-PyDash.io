import React from 'react';
import { Route } from 'react-router-dom';

// Visual:
import { Breadcrumb } from '@pydash/react-breadcrumbs';


/**
 * A special version of the `Route` component that the `react-router-dom` exposes
 * which not only contains a Route handler, but will also add that part of the route to the breadcrumbs of the current page.
 * This means that when multiple of these components are nested in one another, the breadcrumbs of this nesting will show up.
 * (The actual rendering of these breadcrumbs happens in `UserInterface` using the `Breadcrumbs` component)
 */
const BreadcrumbRoute = ({
	  component: Component,
	  includeSearch = false,
    isLink = true,
	  render,
	  ...props
}) => (
    <Route { ...props } render={ routeProps => (
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
