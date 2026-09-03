import pytest
from playwright.sync_api import expect

from pages.cart_page import CartPage
from pages.home_page import HomePage
from pages.product_details_page import ProductDetailsPage
from pages.products_page import ProductsPage


@pytest.mark.smoke
def test_add_product_to_cart_with_specific_quantity(page):
    details = ProductDetailsPage(page)
    details.open(product_id=1)
    details.set_quantity(4)
    details.add_to_cart()
    details.go_to_cart_from_modal()

    cart = CartPage(page)
    expect(cart.cart_rows.first).to_be_visible()
    assert cart.product_count() == 1
    assert "4" in cart.quantity_for_product(1)


@pytest.mark.functional
def test_add_multiple_products_to_cart(page):
    products_page = ProductsPage(page)
    products_page.open()
    products_page.add_product_to_cart_by_index(0)
    products_page.page.locator("button.close-modal").click()
    products_page.add_product_to_cart_by_index(1)
    products_page.page.locator("button.close-modal").click()

    products_page.go_to_cart()

    cart = CartPage(page)
    expect(cart.cart_rows.nth(1)).to_be_visible()
    assert cart.product_count() == 2


@pytest.mark.functional
def test_remove_item_from_cart(page):
    details = ProductDetailsPage(page)
    details.open(product_id=1)
    details.add_to_cart()
    details.go_to_cart_from_modal()

    cart = CartPage(page)
    expect(cart.cart_rows.first).to_be_visible()
    assert cart.product_count() == 1
    cart.remove_product(1)

    cart.row_for_product(1).wait_for(state="detached")
    assert cart.product_count() == 0
    page.reload()
    expect(cart.empty_cart_message).to_be_visible()


@pytest.mark.regression
def test_recommended_items_appears_on_homepage(page):
    # NOTE: the official test case (#22) documents this section on /view_cart, but the live
    # site currently only renders it on the homepage — see docs/test_plan.md and the linked
    # GitHub issue for the discrepancy.
    home = HomePage(page)
    home.open()

    home.recommended_items.scroll_into_view_if_needed()
    expect(home.recommended_items).to_be_visible()
