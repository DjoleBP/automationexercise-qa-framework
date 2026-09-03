from playwright.sync_api import Page

from pages.base_page import BasePage
from utils.data_factory import UserData


class SignupPage(BasePage):
    """The 'Enter Account Information' form shown after the initial name/email step."""

    def __init__(self, page: Page):
        super().__init__(page)
        self.title_mr = page.locator("#id_gender1")
        self.title_mrs = page.locator("#id_gender2")
        self.password_input = page.locator('[data-qa="password"]')
        self.days_select = page.locator("#days")
        self.months_select = page.locator("#months")
        self.years_select = page.locator("#years")
        self.newsletter_checkbox = page.locator("#newsletter")
        self.optin_checkbox = page.locator("#optin")
        self.first_name_input = page.locator('[data-qa="first_name"]')
        self.last_name_input = page.locator('[data-qa="last_name"]')
        self.company_input = page.locator('[data-qa="company"]')
        self.address1_input = page.locator('[data-qa="address"]')
        self.address2_input = page.locator('[data-qa="address2"]')
        self.country_select = page.locator("#country")
        self.state_input = page.locator('[data-qa="state"]')
        self.city_input = page.locator('[data-qa="city"]')
        self.zipcode_input = page.locator('[data-qa="zipcode"]')
        self.mobile_number_input = page.locator('[data-qa="mobile_number"]')
        self.create_account_button = page.locator('[data-qa="create-account"]')
        self.account_created_heading = page.get_by_text("ACCOUNT CREATED!")
        self.continue_button = page.locator("[data-qa='continue-button']")

    def fill_account_information(self, user: UserData):
        (self.title_mr if user.title == "Mr" else self.title_mrs).check()
        self.password_input.fill(user.password)
        self.days_select.select_option(user.birth_day)
        self.months_select.select_option(user.birth_month)
        self.years_select.select_option(user.birth_year)
        self.first_name_input.fill(user.first_name)
        self.last_name_input.fill(user.last_name)
        self.company_input.fill(user.company)
        self.address1_input.fill(user.address1)
        self.address2_input.fill(user.address2)
        self.country_select.select_option(user.country)
        self.state_input.fill(user.state)
        self.city_input.fill(user.city)
        self.zipcode_input.fill(user.zipcode)
        self.mobile_number_input.fill(user.mobile_number)

    def submit(self):
        self.create_account_button.click()

    def continue_after_account_created(self):
        self.continue_button.click()
