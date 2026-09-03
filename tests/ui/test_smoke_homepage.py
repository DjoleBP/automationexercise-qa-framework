import pytest
from playwright.sync_api import Page

from pages.base_page import BasePage


@pytest.mark.smoke
def test_homepage_loads(page: Page):
    home = BasePage(page)
    home.goto("/")

    assert "Automation Exercise" in home.title()
    assert page.locator("div.logo").first.is_visible()
