import pytest

from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage, PaymentPage
from pages.product_details_page import ProductDetailsPage


@pytest.mark.smoke
def test_checkout_flow_up_to_order_confirmation(logged_in_page, registered_user):
    page = logged_in_page

    details = ProductDetailsPage(page)
    details.open(product_id=1)
    details.add_to_cart()
    details.go_to_cart_from_modal()

    cart = CartPage(page)
    cart.proceed_to_checkout()

    checkout = CheckoutPage(page)
    checkout.add_order_comment("Please deliver in the morning.")
    checkout.place_order()

    payment = PaymentPage(page)
    payment.pay_with_dummy_card(registered_user.name)

    assert payment.order_confirmation_message.is_visible()
