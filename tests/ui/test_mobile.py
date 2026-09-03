import pytest
from playwright.sync_api import expect

from pages.home_page import HomePage
from pages.products_page import ProductsPage


@pytest.mark.mobile
@pytest.mark.smoke
def test_homepage_loads_on_mobile(mobile_page):
    home = HomePage(mobile_page)
    home.open()

    assert "Automation Exercise" in home.title()
    expect(home.logo).to_be_visible()


@pytest.mark.mobile
@pytest.mark.functional
def test_product_browse_on_mobile(mobile_page):
    products_page = ProductsPage(mobile_page)
    products_page.open()

    expect(products_page.products_title).to_be_visible()
    expect(products_page.product_cards.first).to_be_visible()


@pytest.mark.mobile
@pytest.mark.functional
def test_search_on_mobile(mobile_page):
    products_page = ProductsPage(mobile_page)
    products_page.open()
    products_page.search_for("Top")

    expect(products_page.searched_products_title).to_be_visible()
    expect(products_page.product_cards.first).to_be_visible()
