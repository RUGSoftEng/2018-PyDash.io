Components
----------

**src/App.js**

### 1. App




Property | Type | Required | Default value | Description
:--- | :--- | :--- | :--- | :---
username|string|no||
isAuthenticated|bool|yes||
-----
**src/Notifier.js**

### 1. Notifier

This component ensures the snackbar notification bar functions correctly,
 for example by making it visible long enough to be readable   




-----
**src/Routes.js**

### 1. Routes

Purpose: Shows the correct pages when the link is matching one of the switch statements.   




Property | Type | Required | Default value | Description
:--- | :--- | :--- | :--- | :---
username|string|no||
isAuthenticated|bool|yes||
signInHandler|func|yes||
signOutHandler|func|yes||
-----
**src/app/main_interface/Notifications.js/snackbars.js**

### 1. SimpleSnackbar

Outdated   




Property | Type | Required | Default value | Description
:--- | :--- | :--- | :--- | :---
classes|object|yes||
-----
**src/app/statistics/Statistics.js**

### 1. Statistics

Outdated   




-----
**src/authenticated_app/AuthenticatedApp.js**

### 1. AuthenticatedApp

Base of the app after logging in. Renders the user interface and the relevant page for the current URL.
Also handles the updating of data for the dashboards linked to the logged in account.   




Property | Type | Required | Default value | Description
:--- | :--- | :--- | :--- | :---
username|string|yes||
isAuthenticated|bool|yes||
signOutHandler|func|yes||
-----
**src/authenticated_app/AuthenticatedRoutes.js**

### 1. AuthenticatedRoutes

Same purpose as Routes.js, routing, but for the website after authentication. The routes after a certain dashboard are
handled by DashboardRoutes.js.   




Property | Type | Required | Default value | Description
:--- | :--- | :--- | :--- | :---
dashboards|object|no||
-----
**src/authenticated_app/dashboard/DashboardRoutes.js**

### 1. DashboardRoutes




Property | Type | Required | Default value | Description
:--- | :--- | :--- | :--- | :---
dashboard|shape|no||
match|shape|no||
-----
**src/authenticated_app/dashboard/statistics_page/EndpointExecutionTimesPanel.js**

### 1. EndpointExecutionTimesPanel




Property | Type | Required | Default value | Description
:--- | :--- | :--- | :--- | :---
dashboard_id|string|yes||
-----
**src/authenticated_app/dashboard/statistics_page/ExecutionTimesGraph.js**

### 1. ExecutionTimesGraph




Property | Type | Required | Default value | Description
:--- | :--- | :--- | :--- | :---
data|array|yes||
title|string|yes||
-----
**src/authenticated_app/dashboard/statistics_page/StatisticFetcher.js**

### 1. StatisticFetcher




Property | Type | Required | Default value | Description
:--- | :--- | :--- | :--- | :---
timeslice|string|no||
-----
**src/authenticated_app/dashboard/statistics_page/StatisticsPage.js**

### 1. StatisticsPage




Property | Type | Required | Default value | Description
:--- | :--- | :--- | :--- | :---
theme|object|yes||
dashboard|shape|yes||
-----
**src/authenticated_app/dashboard/statistics_page/TimesliceTabs.js**

### 1. TimesliceTabs




-----
**src/authenticated_app/dashboard/statistics_page/UniqueVisitorsHeatmapPanel.js**

### 1. UniqueVisitorsHeatmapPanel




Property | Type | Required | Default value | Description
:--- | :--- | :--- | :--- | :---
dashboard_id|string|yes||
-----
**src/authenticated_app/dashboard/statistics_page/UniqueVisitorsPanel.js**

### 1. UniqueVisitorsPanel




Property | Type | Required | Default value | Description
:--- | :--- | :--- | :--- | :---
dashboard_id|string|yes||
-----
**src/authenticated_app/dashboard/statistics_page/VisitorsHeatmapGraph.js**

### 1. VisitorsHeatmapGraph




Property | Type | Required | Default value | Description
:--- | :--- | :--- | :--- | :---
data|array|yes||
title|string|yes||
-----
**src/authenticated_app/dashboard/statistics_page/VisitorsHeatmapPanel.js**

### 1. VisitorsHeatmapPanel




Property | Type | Required | Default value | Description
:--- | :--- | :--- | :--- | :---
dashboard_id|string|yes||
-----
**src/authenticated_app/dashboard/statistics_page/VisitsGraph.js**

### 1. VisitsGraph




Property | Type | Required | Default value | Description
:--- | :--- | :--- | :--- | :---
data|array|yes||
title|string|yes||
tooltip_title|string|yes||
height|number|yes||
timeslice|string|yes||
-----
**src/authenticated_app/dashboard/statistics_page/VisitsPanel.js**

### 1. VisitsPanel




Property | Type | Required | Default value | Description
:--- | :--- | :--- | :--- | :---
dashboard_id|string|yes||
-----
**src/authenticated_app/endpoint/Endpoint.js**

### 1. Endpoint




-----
**src/authenticated_app/endpoint/EndpointsTable.js**

### 1. EndpointsTable




-----
**src/authenticated_app/overview/AddDashboardDialog.js**

### 1. AddDashboardDialog




-----
**src/authenticated_app/overview/DashboardList.js**

### 1. DashboardList




-----
**src/authenticated_app/overview/DashboardListItem.js**

### 1. DashboardListItem




-----
**src/authenticated_app/overview/OverviewPage.js**

### 1. OverviewPage




-----
**src/authenticated_app/settings/SettingsPage.js**

### 1. SettingsPage

Component representing the settings page. Provides rendering and functionality for changing account details, enabling 
disabling sounds, and removing user accounts.   




Property | Type | Required | Default value | Description
:--- | :--- | :--- | :--- | :---
classes|object|yes||
-----
**src/authenticated_app/user_interface/Logout.js**

### 1. Logout

Renders the logout icon, handles logout requests and redirects to the login page when succesful.   




Property | Type | Required | Default value | Description
:--- | :--- | :--- | :--- | :---
signOutHandler|func|yes||
-----
**src/authenticated_app/user_interface/Menu.js**

### 1. MainMenuItems




### 2. OtherMenuItems




-----
**src/authenticated_app/user_interface/UserInterface.js**

### 1. UserInterface

Shows the user interface for logged in users, including the sidebar with links to the overview and the settings page.   




Property | Type | Required | Default value | Description
:--- | :--- | :--- | :--- | :---
classes|object|yes||
theme|object|yes||
-----
**src/common/BreadcrumbRoute.js**

### 1. BreadcrumbRoute




Property | Type | Required | Default value | Description
:--- | :--- | :--- | :--- | :---
includeSearch||no|false|
isLink||no|true|
-----
**src/common/ResponsiveGraphWrapper.js**

### 1. ResponsiveGraphWrapper

Wrapper for the graphs, making sure they are shown the right way   




Property | Type | Required | Default value | Description
:--- | :--- | :--- | :--- | :---
height|number|yes||
-----
**src/common/WidthAwareContainer.js**

### 1. WidthAwareContainer

This component becomes as large as its container, and then passes its resulting `width` on as the `with` prop to its child,
as to make child components that require a width in pixels responsive.   




-----
**src/login/LoginPage.js**

### 1. LoginPage

Purpose: Renders the login page and handles the login requests. Lets the user know if something went wrong with logging in,
warns the user about an unsafe password if he has one and contains a link to the register page.   




Property | Type | Required | Default value | Description
:--- | :--- | :--- | :--- | :---
signInHandler|func|yes||
-----
**src/login/ProtectedRoute.js**

### 1. ProtectedRoute




-----
**src/registration/RegistrationPage.js**

### 1. RegistrationPage

Renders the registration page. Also handles the register request itself, including making sure all the necessary fields
are filled in correctly. Shows relevant error messages when something is going wrong and provides an explanation on
the required security for passwords.   




Property | Type | Required | Default value | Description
:--- | :--- | :--- | :--- | :---
signInHandler|func|yes||
-----
**src/registration/VerificationPage.js**

### 1. VerificationPage

Renders the verification page new accounts are sent to after clicking on the vericiation link in their e-mail
.   




-----

<sub>This document was generated by the <a href="https://github.com/marborkowski/react-doc-generator" target="_blank">**React DOC Generator v1.2.5**</a>.</sub>
