from playwright.sync_api import Page

from pages.base_page import BasePage


class ProductDetailsPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.product_name = page.locator("div.product-information h2")
        self.category = page.locator("div.product-information p").filter(has_text="Category:")
        self.price = page.locator("div.product-information span span").first
        self.availability = page.locator("div.product-information p").filter(has_text="Availability:")
        self.condition = page.locator("div.product-information p").filter(has_text="Condition:")
        self.brand = page.locator("div.product-information p").filter(has_text="Brand:")
        self.quantity_input = page.locator("#quantity")
        self.add_to_cart_button = page.locator("button.cart")
        self.view_cart_link = page.locator('div.modal-body a[href="/view_cart"]')

    def open(self, product_id: int):
        self.goto(f"/product_details/{product_id}")

    def set_quantity(self, quantity: int):
        self.quantity_input.fill(str(quantity))

    def add_to_cart(self):
        self.add_to_cart_button.click()

    def go_to_cart_from_modal(self):
        self.view_cart_link.click()
