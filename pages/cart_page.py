from playwright.sync_api import Page

from pages.base_page import BasePage


class CartPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.cart_rows = page.locator("tr[id^='product-']")
        self.empty_cart_message = page.get_by_text("Cart is empty!")
        self.proceed_to_checkout_button = page.get_by_text("Proceed To Checkout")

    def open(self):
        self.goto("/view_cart")

    def row_for_product(self, product_id: int):
        return self.page.locator(f"#product-{product_id}")

    def quantity_for_product(self, product_id: int) -> str:
        return self.row_for_product(product_id).locator("td.cart_quantity button").inner_text()

    def price_for_product(self, product_id: int) -> str:
        return self.row_for_product(product_id).locator("td.cart_price p").inner_text()

    def remove_product(self, product_id: int):
        self.row_for_product(product_id).locator("a.cart_quantity_delete").click()

    def product_count(self) -> int:
        return self.cart_rows.count()

    def proceed_to_checkout(self):
        self.proceed_to_checkout_button.click()
