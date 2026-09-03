import pytest

from pages.home_page import HomePage
from pages.login_page import LoginPage


@pytest.mark.smoke
def test_login_with_valid_credentials(page, registered_user):
    home = HomePage(page)
    home.open()
    home.go_to_login()

    login_page = LoginPage(page)
    login_page.login(registered_user.email, registered_user.password)

    assert home.is_logged_in_as(registered_user.name)


@pytest.mark.smoke
def test_logout_returns_to_logged_out_state(logged_in_page):
    home = HomePage(logged_in_page)
    home.logout()

    login_page = LoginPage(logged_in_page)
    assert login_page.login_button.is_visible()
    assert home.login_signup_link.is_visible()


@pytest.mark.negative
def test_login_with_wrong_password(page, registered_user):
    home = HomePage(page)
    home.open()
    home.go_to_login()

    login_page = LoginPage(page)
    login_page.login(registered_user.email, "WrongPassword123!")

    assert login_page.login_error.is_visible()
    assert not home.is_logged_in_as(registered_user.name)


@pytest.mark.negative
def test_login_with_unregistered_email(page):
    home = HomePage(page)
    home.open()
    home.go_to_login()

    login_page = LoginPage(page)
    login_page.login("does_not_exist_qaframework@example.com", "SomePassword123!")

    assert login_page.login_error.is_visible()
