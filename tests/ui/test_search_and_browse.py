import pytest

from pages.product_details_page import ProductDetailsPage
from pages.products_page import ProductsPage


@pytest.mark.smoke
def test_search_for_existing_product(page):
    products_page = ProductsPage(page)
    products_page.open()
    products_page.search_for("Top")

    assert products_page.searched_products_title.is_visible()
    assert products_page.product_cards.count() > 0
    names = products_page.visible_product_names()
    assert any("top" in name.lower() for name in names)


@pytest.mark.negative
def test_search_with_no_matches_shows_no_products(page):
    products_page = ProductsPage(page)
    products_page.open()
    products_page.search_for("zzznonexistentproductxyz")

    assert products_page.searched_products_title.is_visible()
    assert products_page.product_cards.count() == 0


@pytest.mark.regression
def test_product_details_page_shows_expected_fields(page):
    products_page = ProductsPage(page)
    products_page.open()
    products_page.open_product_details_by_index(0)

    details = ProductDetailsPage(page)
    assert details.product_name.is_visible()
    assert details.category.is_visible()
    assert details.price.is_visible()
    assert details.availability.is_visible()
    assert details.condition.is_visible()
    assert details.brand.is_visible()


@pytest.mark.regression
def test_category_filter_returns_filtered_results(page):
    products_page = ProductsPage(page)
    products_page.open()
    products_page.go_to_category("/category_products/1")

    assert products_page.product_cards.count() > 0


@pytest.mark.regression
def test_brand_filter_returns_filtered_results(page):
    products_page = ProductsPage(page)
    products_page.open()
    products_page.go_to_brand("Polo")

    assert products_page.product_cards.count() > 0
    names = products_page.visible_product_names()
    assert len(names) > 0
