from playwright.sync_api import Page, expect

from utils.config import BASE_URL


class BasePage:
    """Chrome shared across the site: the header navigation and the add-to-cart modal."""

    def __init__(self, page: Page):
        self.page = page
        self.login_signup_link = page.locator('a[href="/login"]')
        self.logout_link = page.locator('a[href="/logout"]')
        self.delete_account_link = page.locator('a[href="/delete_account"]')
        self.products_link = page.locator('a[href="/products"]').first
        self.cart_link = page.locator('a[href="/view_cart"]').first
        self.close_modal_button = page.locator("button.close-modal")

    def goto(self, path: str = "/"):
        self.page.goto(f"{BASE_URL}{path}")

    def title(self) -> str:
        return self.page.title()

    def go_to_login(self):
        self.login_signup_link.click()

    def go_to_products(self):
        self.products_link.click()

    def go_to_cart(self):
        self.cart_link.click()

    def close_modal(self):
        """Dismisses the "Added!" confirmation modal.

        Required between consecutive add-to-cart clicks: the modal's backdrop covers the
        page and swallows the next click.
        """
        self.close_modal_button.click()

    def logout(self):
        self.logout_link.click()

    def delete_account(self):
        self.delete_account_link.click()

    def is_logged_in_as(self, name: str) -> bool:
        return self.page.get_by_text(f"Logged in as {name}").is_visible()

    def expect_logged_in_as(self, name: str):
        """Waits (with retry) for the "Logged in as <name>" nav text to appear."""
        expect(self.page.get_by_text(f"Logged in as {name}")).to_be_visible()
