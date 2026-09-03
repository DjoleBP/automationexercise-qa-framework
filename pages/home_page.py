from playwright.sync_api import Page

from pages.base_page import BasePage


class HomePage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.logo = page.locator("div.logo")
        self.subscribe_email_input = page.locator("#susbscribe_email")
        self.subscribe_button = page.locator("#subscribe")
        self.subscribe_success_message = page.locator("#success-subscribe")
        self.recommended_items = page.locator("div.recommended_items")

    def open(self):
        self.goto("/")

    def subscribe_to_newsletter(self, email: str):
        self.subscribe_email_input.scroll_into_view_if_needed()
        self.subscribe_email_input.fill(email)
        self.subscribe_button.click()
