from pytest_bdd import (
    given,
    scenario,
    then,
    when,
)
from pytest_bdd import parsers

from pydash_app.user.entity import User
import pydash_app.user as user


@scenario("sign_in.feature", "Signing in successfully as existent user")
def test_sign_in_successful():
    "Signing in successfully as existent user"


@scenario("sign_in.feature", "Signing in without entering anything")
def test_sign_in_empty():
    "Signing in without entering anything"


@scenario("sign_in.feature", "Signing in as unexistent user")
def test_sign_in_unexistent():
    "Signing in as unexistent user"


@scenario("sign_in.feature", "Signing in as existent user without password")
def test_sign_in_nopassword():
    "Signing in as unexistent user without password"


@scenario("sign_in.feature", "Signing in as existent user with a wrong password")
def test_sign_in_wrongpassword():
    "Signing in as existent user with a wrong password"


@given(parsers.cfparse("PyDash contains the user \"{username}\" with password \"{password}\""))
def _(username, password):
    existing_user = User(username, password)
    user.add_to_repository(existing_user)


@when("I visit the Pydash sign in page")
def i_visit_pydash_sign_in_page(browser, testserver):
    browser.visit(testserver.url)


@when(parsers.cfparse("I enter the username \"{username}\""))
def i_enter_username(browser, username):
    browser.find_by_id("username").first.fill(username)


@when(parsers.cfparse("I enter the password \"{password}\""))
def i_enter_password(browser, password):
    browser.find_by_id("password").first.fill(password)


@when("I enter an unexistent username")
def when_i_enter_unexistent_username(browser):
    browser.find_by_id("username").first.fill("idonotexist")


@when(parsers.cfparse(r"I click the sign in button"))
def i_enter_password(browser):
    browser.find_by_css("button").first.click()


@then("I should be on the overview page")
def then_i_should_be_on_the_overview_page(browser):
    pass


@then(parsers.cfparse("I should see the username \"{username}\" in the menu"))
def then_i_should_see_my_username_in_the_menu(browser, username):
    assert browser.is_text_present(username)


@then("I should see the error 'both fields are required'")
def then_i_should_see_error_both_fields_required(browser):
    # assert browser.find_by_id("#password-helper-text").visible
    assert browser.is_text_present("Both fields are required!")


@then("I should see the error 'incorrect credentials'")
def then_i_should_see_error_message(browser):
    assert browser.is_text_present("Incorrect credentials 😱")
