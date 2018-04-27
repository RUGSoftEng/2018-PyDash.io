import pytest
from pytest_bdd import (
    given,
    scenario,
    then,
    when,
)
import time

@scenario("salad_example.feature", "Visiting the Log-In page")
def test_salad_example():
    """Visiting the Log-In Page"""


@when("I visit the Pydash website")
def i_visit_the_pydash_website(browser, testserver):
    browser.visit(testserver.url)

@then("I should see \"Pydash\" somewhere in the page")
def _(browser):
    browser.is_text_present("Pydash")
