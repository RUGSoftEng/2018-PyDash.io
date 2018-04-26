Feature: Ensuring that Lettuce works, and W+K's website loads
In order to make sure that lettuce works
As a developer
I open the Wieden+Kennedy website using lettuce

Scenario: Opening the W+K website works
	Given I visit the url "http://www.wk.com/"
	When I look around
	Then I should see "Wieden+Kennedy" somewhere in the page


