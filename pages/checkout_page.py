from playwright.sync_api import Page

from pages.base_page import BasePage


class CheckoutPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.address_delivery = page.locator("#address_delivery")
        self.comment_textarea = page.locator('textarea[name="message"]')
        self.place_order_button = page.get_by_role("link", name="Place Order")

    def open(self):
        self.goto("/checkout")

    def add_order_comment(self, comment: str):
        self.comment_textarea.fill(comment)

    def place_order(self):
        self.place_order_button.click()


class PaymentPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.name_on_card_input = page.locator('[data-qa="name-on-card"]')
        self.card_number_input = page.locator('[data-qa="card-number"]')
        self.cvc_input = page.locator('[data-qa="cvc"]')
        self.expiry_month_input = page.locator('[data-qa="expiry-month"]')
        self.expiry_year_input = page.locator('[data-qa="expiry-year"]')
        self.pay_button = page.locator('[data-qa="pay-button"]')
        self.order_confirmation_message = page.locator('[data-qa="order-placed"]')

    def pay_with_dummy_card(self, name_on_card: str):
        self.name_on_card_input.fill(name_on_card)
        self.card_number_input.fill("4111111111111111")
        self.cvc_input.fill("123")
        self.expiry_month_input.fill("12")
        self.expiry_year_input.fill("2030")
        self.pay_button.click()
