Feature: Visiting PyDash
In order to make sure that the PyDash Web-application
is usable for everyone,
as a visitor, we visit the Pydash root page
and make sure it can be used.


Scenario: Visiting the Log-In page
	When I visit the Pydash website
	Then I should see "Pydash" somewhere in the page


