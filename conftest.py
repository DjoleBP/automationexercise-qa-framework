import re

import pytest

from pages.home_page import HomePage
from pages.login_page import LoginPage
from utils.api_client import create_account, delete_account
from utils.data_factory import UserData, random_user

AD_URL_PATTERN = re.compile(r"(doubleclick|googlesyndication|google_vignette|adservice|googleads|/ads/)")


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {**browser_context_args, "viewport": {"width": 1366, "height": 900}}


@pytest.fixture
def context(context):
    """Block ad-network requests site-wide: the live site serves interstitial ads that can
    hijack navigation mid-test (e.g. a Google Vignette ad replacing a product-details click)."""
    context.route(AD_URL_PATTERN, lambda route: route.abort())
    return context


@pytest.fixture
def registered_user() -> UserData:
    """Provisions a throwaway account via the API (fast, independent of UI) and deletes it after the test."""
    user = random_user()
    response = create_account(user)
    # The API always answers HTTP 200; the real result lives in the "responseCode" field.
    assert response.json().get("responseCode") == 201, f"createAccount failed: {response.text}"

    yield user

    delete_account(user.email, user.password)


@pytest.fixture
def logged_in_page(page, registered_user: UserData):
    """A page navigated to the homepage with `registered_user` already logged in via the UI."""
    login_page = LoginPage(page)
    login_page.open()
    login_page.login(registered_user.email, registered_user.password)

    home_page = HomePage(page)
    assert home_page.is_logged_in_as(registered_user.name)

    return page
