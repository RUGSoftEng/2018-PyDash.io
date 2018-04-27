import pytest
from pytest_bdd import (
    given,
    scenario,
    then,
    when,
)
from pytest_bdd import parsers

from pydash_app.user.user import User
import pydash_app.user as user

@scenario("sign_in.feature", "Signing in successfully as existent user")
def _():
    pass

@scenario("sign_in.feature", "Signing in without entering anything")
def _():
    pass

@scenario("sign_in.feature", "Signing in as unexistent user")
def _():
    pass

@scenario("sign_in.feature", "Signing in as existent user without password")
def _():
    pass

@scenario("sign_in.feature", "Signing in as existent user with a wrong password")
def _():
    pass

@given(parsers.cfparse("PyDash contains the user \"{username}\" with password {password}"))
def _():
    existing_user = User(username, password)
    user.add_to_repository(existing_user)


@when("I visit the Pydash sign in page")
def _(browser, testserver):
    browser.visit(testserver.url)

@when(parsers.cfparse(r"I enter the username \"{username}\""))
def _(browser, username):
    print(username)
