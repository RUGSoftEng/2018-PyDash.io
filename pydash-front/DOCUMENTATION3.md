Components


-----



-----



**src/App.js**

### App

The entry point of the React application.
Almost all work is delegated to subcomponents.
The only work that the App component itself does, is to check if the user is logged in or not,
and pass functions to lower-level components to sign a user in or out.   




Property | Type | Required | Default value | Description
:--- | :--- | :--- | :--- | :---
username|string|no||
isAuthenticated|bool|yes||


-----


**src/Notifier.js**

### Notifier

This component shows the notifications ('Snackbars') that the app might generate.
This has been put in its own component that is included at the outside of the application,
so that logging in/logging out and other state changes that might completely alter how the page will look,
will be able to show notifications as well.

The Notifier component is not used directly from within the app. Rather, the `showNotification()` function that this component file exports is.
The application should only contain one Notifier component, because the `showNotification()` function expects there to only be one Notifier.   






-----


**src/Routes.js**

### Routes

Will dispatch between the various top-level routes that the application uses.

After having logged in, there are various sub-routes, which are dispatched in their own component, inside of AuthenticatedApp.   




Property | Type | Required | Default value | Description
:--- | :--- | :--- | :--- | :---
username|string|no||
isAuthenticated|bool|yes||
signInHandler|func|yes||
signOutHandler|func|yes||


-----


**src/authenticated_app/AuthenticatedApp.js**

### AuthenticatedApp

Base of the app after logging in. Renders the user interface and the relevant page for the current path.
Also handles the updating of data for the dashboards linked to the logged in account.   




Property | Type | Required | Default value | Description
:--- | :--- | :--- | :--- | :---
username|string|yes||
isAuthenticated|bool|yes||
signOutHandler|func|yes||


-----


**src/authenticated_app/AuthenticatedRoutes.js**

### AuthenticatedRoutes

Similar to `Routes`, this component performs routing, but for the website after being authenticated.   




Property | Type | Required | Default value | Description
:--- | :--- | :--- | :--- | :---
dashboards|object|no||


-----


**src/authenticated_app/dashboard/DashboardRoutes.js**

### DashboardRoutes

Dispatches between all routes concerning a single dashboard.   




Property | Type | Required | Default value | Description
:--- | :--- | :--- | :--- | :---
dashboard|shape|no||
match|shape|no||


-----


**src/authenticated_app/dashboard/statistics_page/EndpointExecutionTimesPanel.js**

### EndpointExecutionTimesPanel

Panel containing the `EndpointExecutionTimesGraph`.   




Property | Type | Required | Default value | Description
:--- | :--- | :--- | :--- | :---
dashboard_id|string|yes||


-----


**src/authenticated_app/dashboard/statistics_page/ExecutionTimesGraph.js**

### ExecutionTimesGraph

Displays the average execution time per the given dashboard's endpoint.   




Property | Type | Required | Default value | Description
:--- | :--- | :--- | :--- | :---
data|array|yes||
title|string|yes||


-----


**src/authenticated_app/dashboard/statistics_page/StatisticFetcher.js**

### StatisticFetcher

Base class component that specific Statistics-fetchers inherit.   




Property | Type | Required | Default value | Description
:--- | :--- | :--- | :--- | :---
timeslice|string|no||


-----


**src/authenticated_app/dashboard/statistics_page/StatisticsPage.js**

### StatisticsPage

The main Dashboard page that cointains all general statistics we've gathered for it.   




Property | Type | Required | Default value | Description
:--- | :--- | :--- | :--- | :---
theme|object|yes||
dashboard|shape|yes||


-----


**src/authenticated_app/dashboard/statistics_page/TimesliceTabs.js**

### TimesliceTabs

A component put inside this component will receive the `timeslice` property

This property is set, depending on the tab that the user selects (one of hour, day, week, month, year)   






-----


**src/authenticated_app/dashboard/statistics_page/UniqueVisitorsHeatmapPanel.js**

### UniqueVisitorsHeatmapPanel

Panel containing a heatmap of all unique visitors that have been visiting this Dashboard.   




Property | Type | Required | Default value | Description
:--- | :--- | :--- | :--- | :---
dashboard_id|string|yes||


-----


**src/authenticated_app/dashboard/statistics_page/UniqueVisitorsPanel.js**

### UniqueVisitorsPanel

A Panel containing a line graph showing how many unique visitors this Dashboard had.   




Property | Type | Required | Default value | Description
:--- | :--- | :--- | :--- | :---
dashboard_id|string|yes||


-----


**src/authenticated_app/dashboard/statistics_page/VisitorsHeatmapGraph.js**

### VisitorsHeatmapGraph

Heatmap of visitors that have been visiting this Dashboard.   




Property | Type | Required | Default value | Description
:--- | :--- | :--- | :--- | :---
data|array|yes||
title|string|yes||


-----


**src/authenticated_app/dashboard/statistics_page/VisitorsHeatmapPanel.js**

### VisitorsHeatmapPanel

Panel containing a heatmap of all visitors that have been visiting this Dashboard.   




Property | Type | Required | Default value | Description
:--- | :--- | :--- | :--- | :---
dashboard_id|string|yes||


-----


**src/authenticated_app/dashboard/statistics_page/VisitsGraph.js**

### VisitsGraph

A line graph showing how many visitors this Dashboard had.   




Property | Type | Required | Default value | Description
:--- | :--- | :--- | :--- | :---
data|array|yes||
title|string|yes||
tooltip_title|string|yes||
height|number|yes||
timeslice|string|yes||


-----


**src/authenticated_app/dashboard/statistics_page/VisitsPanel.js**

### VisitsPanel

A Panel containing a line graph showing how many visitors this Dashboard had.   




Property | Type | Required | Default value | Description
:--- | :--- | :--- | :--- | :---
dashboard_id|string|yes||


-----


**src/authenticated_app/endpoint/EndpointPage.js**

### EndpointPage

The `EndpointPage` renders the details page of a single EndpointPage.   






-----


**src/authenticated_app/endpoint/EndpointsTable.js**

### EndpointsTable






-----


**src/authenticated_app/overview/AddDashboardDialog.js**

### AddDashboardDialog

`AddDashboardDialog` shows the modal dialog that allows a user to add a new dashboard to PyDash.
It also performs the handling logic of saving the information that has been entered in the form.   






-----


**src/authenticated_app/overview/DashboardList.js**

### DashboardList

A list of dashboards, where each entry (`DashboardListItem`) contains some general information about the dashboard.   






-----


**src/authenticated_app/overview/DashboardListItem.js**

### DashboardListItem

The `DashboardListItem` displays some general information about the given dashboard;

This component is to be used as part of a `DashboardList`.   






-----


**src/authenticated_app/overview/OverviewPage.js**

### OverviewPage

The `OverviewPage` is the main page the user sees after logging in.   






-----


**src/authenticated_app/settings/SettingsPage.js**

### SettingsPage

Component representing the settings page.

Provides rendering and functionality for changing account details, enabling
disabling sounds, and removing user accounts.   




Property | Type | Required | Default value | Description
:--- | :--- | :--- | :--- | :---
classes|object|yes||


-----


**src/authenticated_app/user_interface/Logout.js**

### Logout

Renders the logout icon, handles logout requests and redirects to the login page when succesful.   




Property | Type | Required | Default value | Description
:--- | :--- | :--- | :--- | :---
signOutHandler|func|yes||


-----


**src/authenticated_app/user_interface/Menu.js**

### MainMenuItems




### 2. OtherMenuItems






-----


**src/authenticated_app/user_interface/UserInterface.js**

### UserInterface

Shows the user interface for logged in users:

- The top menu
- The side menu that is used for navigation (whose contents live in `Menu.js`)
- The `Breadcrumbs` of the currently shown page.   




Property | Type | Required | Default value | Description
:--- | :--- | :--- | :--- | :---
classes|object|yes||
theme|object|yes||


-----


**src/common/BreadcrumbRoute.js**

### BreadcrumbRoute

A special version of the `Route` component that the `react-router-dom` exposes
which not only contains a Route handler, but will also add that part of the route to the breadcrumbs of the current page.
This means that when multiple of these components are nested in one another, the breadcrumbs of this nesting will show up.
(The actual rendering of these breadcrumbs happens in `UserInterface` using the `Breadcrumbs` component)   




Property | Type | Required | Default value | Description
:--- | :--- | :--- | :--- | :---
includeSearch||no|false|
isLink||no|true|


-----


**src/common/ResponsiveGraphWrapper.js**

### ResponsiveGraphWrapper

A Nivo Graph component (or other component that you want to auto-resize to fill its container width), can be added to this component to ensure that this resizing will happen.

This component will pass on the 'width' prop to the child, which will be set to the measured width the component ('s container, the ResponsiveGraphWrapper itself) currently has on the page.   




Property | Type | Required | Default value | Description
:--- | :--- | :--- | :--- | :---
height|number|yes||


-----


**src/login/LoginPage.js**

### LoginPage

Renders the login page and handles the login requests. Lets the user know if something went wrong with logging in,
warns the user about an unsafe password if he has one and contains a link to the register page.   




Property | Type | Required | Default value | Description
:--- | :--- | :--- | :--- | :---
signInHandler|func|yes||


-----


**src/registration/RegistrationPage.js**

### RegistrationPage

Renders the registration page. Also handles the register request itself, including making sure all the necessary fields
are filled in correctly. Shows relevant error messages when something is going wrong and provides an explanation on
the required security for passwords.   




Property | Type | Required | Default value | Description
:--- | :--- | :--- | :--- | :---
signInHandler|func|yes||


-----


**src/registration/VerificationPage.js**

### VerificationPage

Renders the verification page new accounts are sent to after clicking on the vericiation link in their e-mail.   






-----



<sub>This document was generated by the <a href="https://github.com/marborkowski/react-doc-generator" target="_blank">**React DOC Generator v1.2.5**</a>.</sub>
