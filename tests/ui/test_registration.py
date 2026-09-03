import pytest
from playwright.sync_api import expect

from pages.home_page import HomePage
from pages.login_page import LoginPage
from pages.signup_page import SignupPage
from utils.api_client import delete_account
from utils.data_factory import random_user


@pytest.mark.smoke
def test_register_new_user_with_valid_data(page):
    user = random_user()

    home = HomePage(page)
    home.open()
    home.go_to_login()

    login_page = LoginPage(page)
    login_page.start_signup(user.name, user.email)

    signup_page = SignupPage(page)
    signup_page.fill_account_information(user)
    signup_page.submit()

    expect(signup_page.account_created_heading).to_be_visible()
    signup_page.continue_after_account_created()

    home.expect_logged_in_as(user.name)

    delete_account(user.email, user.password)


@pytest.mark.negative
def test_register_with_already_registered_email(page, registered_user):
    home = HomePage(page)
    home.open()
    home.go_to_login()

    login_page = LoginPage(page)
    login_page.start_signup("Another Name", registered_user.email)

    expect(login_page.signup_error).to_be_visible()
