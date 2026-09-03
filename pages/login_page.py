from playwright.sync_api import Page

from pages.base_page import BasePage


class LoginPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.login_email_input = page.locator('[data-qa="login-email"]')
        self.login_password_input = page.locator('[data-qa="login-password"]')
        self.login_button = page.locator('[data-qa="login-button"]')
        self.login_error = page.get_by_text("Your email or password is incorrect!")

        self.signup_name_input = page.locator('[data-qa="signup-name"]')
        self.signup_email_input = page.locator('[data-qa="signup-email"]')
        self.signup_button = page.locator('[data-qa="signup-button"]')
        self.signup_error = page.get_by_text("Email Address already exist!")

    def open(self):
        self.goto("/login")

    def login(self, email: str, password: str):
        self.login_email_input.fill(email)
        self.login_password_input.fill(password)
        self.login_button.click()

    def start_signup(self, name: str, email: str):
        self.signup_name_input.fill(name)
        self.signup_email_input.fill(email)
        self.signup_button.click()
