import pytest
from playwright.sync_api import expect

from pages.home_page import HomePage
from pages.login_page import LoginPage


@pytest.mark.smoke
def test_login_with_valid_credentials(page, registered_user):
    home = HomePage(page)
    home.open()
    home.go_to_login()

    login_page = LoginPage(page)
    login_page.login(registered_user.email, registered_user.password)

    home.expect_logged_in_as(registered_user.name)


@pytest.mark.smoke
def test_logout_returns_to_logged_out_state(logged_in_page):
    home = HomePage(logged_in_page)
    home.logout()

    login_page = LoginPage(logged_in_page)
    expect(login_page.login_button).to_be_visible()
    expect(home.login_signup_link).to_be_visible()


@pytest.mark.negative
def test_login_with_wrong_password(page, registered_user):
    home = HomePage(page)
    home.open()
    home.go_to_login()

    login_page = LoginPage(page)
    login_page.login(registered_user.email, "WrongPassword123!")

    expect(login_page.login_error).to_be_visible()
    assert not home.is_logged_in_as(registered_user.name)


@pytest.mark.negative
def test_login_with_unregistered_email(page):
    home = HomePage(page)
    home.open()
    home.go_to_login()

    login_page = LoginPage(page)
    login_page.login("does_not_exist_qaframework@example.com", "SomePassword123!")

    expect(login_page.login_error).to_be_visible()
