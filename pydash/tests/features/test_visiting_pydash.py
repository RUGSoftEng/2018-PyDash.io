import pytest
from pytest_bdd import (
    given,
    scenario,
    then,
    when,
)
import time

@scenario("visiting_pydash.feature", "Visiting the Log-In page")
def test_visiting_pydash():
    """Visiting the Log-In Page"""


@when("I visit the Pydash website")
def _(browser, testserver):
    browser.visit(testserver.url)

@then("I should see \"Pydash\" somewhere in the page")
def _(browser):
    browser.is_text_present("Pydash")
