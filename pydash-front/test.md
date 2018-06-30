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




-----
**src/Routes.js**

### 1. Routes




Property | Type | Required | Default value | Description
:--- | :--- | :--- | :--- | :---
username|string|no||
isAuthenticated|bool|yes||
signInHandler|func|yes||
signOutHandler|func|yes||
-----
**src/app/main_interface/Notifications.js/snackbars.js**

### 1. SimpleSnackbar




Property | Type | Required | Default value | Description
:--- | :--- | :--- | :--- | :---
classes|object|yes||
-----
**src/app/statistics/Statistics.js**

### 1. Statistics




-----
**src/authenticated_app/AuthenticatedApp.js**

### 1. AuthenticatedApp




Property | Type | Required | Default value | Description
:--- | :--- | :--- | :--- | :---
username|string|yes||
isAuthenticated|bool|yes||
signOutHandler|func|yes||
-----
**src/authenticated_app/AuthenticatedRoutes.js**

### 1. AuthenticatedRoutes




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




Property | Type | Required | Default value | Description
:--- | :--- | :--- | :--- | :---
classes|object|yes||
-----
**src/authenticated_app/user_interface/Logout.js**

### 1. Logout




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




Property | Type | Required | Default value | Description
:--- | :--- | :--- | :--- | :---
height|number|yes||
-----
**src/common/WidthAwareContainer.js**

### 1. WidthAwareContainer




-----
**src/login/LoginPage.js**

### 1. LoginPage




Property | Type | Required | Default value | Description
:--- | :--- | :--- | :--- | :---
signInHandler|func|yes||
-----
**src/login/ProtectedRoute.js**

### 1. ProtectedRoute




-----
**src/registration/RegistrationPage.js**

### 1. RegistrationPage




Property | Type | Required | Default value | Description
:--- | :--- | :--- | :--- | :---
signInHandler|func|yes||
-----
**src/registration/VerificationPage.js**

### 1. VerificationPage




-----

<sub>This document was generated by the <a href="https://github.com/marborkowski/react-doc-generator" target="_blank">**React DOC Generator v1.2.5**</a>.</sub>
