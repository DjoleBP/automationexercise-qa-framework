import pytest
from playwright.sync_api import expect

from pages.product_details_page import ProductDetailsPage
from pages.products_page import ProductsPage


@pytest.mark.smoke
def test_search_for_existing_product(page):
    products_page = ProductsPage(page)
    products_page.open()
    products_page.search_for("Top")

    expect(products_page.searched_products_title).to_be_visible()
    expect(products_page.product_cards.first).to_be_visible()
    names = products_page.visible_product_names()
    assert any("top" in name.lower() for name in names)


@pytest.mark.negative
def test_search_with_no_matches_shows_no_products(page):
    products_page = ProductsPage(page)
    products_page.open()
    products_page.search_for("zzznonexistentproductxyz")

    expect(products_page.searched_products_title).to_be_visible()
    assert products_page.product_cards.count() == 0


@pytest.mark.regression
def test_product_details_page_shows_expected_fields(page):
    products_page = ProductsPage(page)
    products_page.open()
    products_page.open_product_details_by_index(0)

    details = ProductDetailsPage(page)
    expect(details.product_name).to_be_visible()
    expect(details.category).to_be_visible()
    expect(details.price).to_be_visible()
    expect(details.availability).to_be_visible()
    expect(details.condition).to_be_visible()
    expect(details.brand).to_be_visible()


@pytest.mark.regression
def test_category_filter_returns_filtered_results(page):
    products_page = ProductsPage(page)
    products_page.open()
    products_page.go_to_category("/category_products/1")

    expect(products_page.product_cards.first).to_be_visible()


@pytest.mark.regression
def test_brand_filter_returns_filtered_results(page):
    products_page = ProductsPage(page)
    products_page.open()
    products_page.go_to_brand("Polo")

    expect(products_page.product_cards.first).to_be_visible()
    names = products_page.visible_product_names()
    assert len(names) > 0
