import re

import pytest

from pages.home_page import HomePage
from pages.login_page import LoginPage
from utils.data_factory import UserData

AD_URL_PATTERN = re.compile(r"(doubleclick|googlesyndication|google_vignette|adservice|googleads|/ads/)")


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {**browser_context_args, "viewport": {"width": 1366, "height": 900}}


@pytest.fixture(autouse=True)
def _block_ads(page):
    """Block ad-network requests: the live site serves interstitial ads that can hijack
    navigation mid-test (e.g. a Google Vignette ad replacing a product-details click).

    Deliberately routes on `page` rather than overriding the `context` fixture -- the latter
    breaks pytest-playwright's automatic --browser cross-browser parametrization.
    """
    page.route(AD_URL_PATTERN, lambda route: route.abort())


@pytest.fixture
def mobile_page(playwright, browser):
    """A page emulating an iPhone 13 (viewport, touch, user agent) for mobile-emulation coverage."""
    device = playwright.devices["iPhone 13"]
    context = browser.new_context(**device)
    context.route(AD_URL_PATTERN, lambda route: route.abort())
    page = context.new_page()

    yield page

    context.close()


@pytest.fixture
def logged_in_page(page, registered_user: UserData):
    """A page navigated to the homepage with `registered_user` already logged in via the UI."""
    login_page = LoginPage(page)
    login_page.open()
    login_page.login(registered_user.email, registered_user.password)

    home_page = HomePage(page)
    home_page.expect_logged_in_as(registered_user.name)

    return page
