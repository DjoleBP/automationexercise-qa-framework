from playwright.sync_api import Page

from pages.base_page import BasePage
from utils.data_factory import ContactMessage


class ContactUsPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.name_input = page.locator('[data-qa="name"]')
        self.email_input = page.locator('[data-qa="email"]')
        self.subject_input = page.locator('[data-qa="subject"]')
        self.message_textarea = page.locator('[data-qa="message"]')
        self.submit_button = page.locator('[data-qa="submit-button"]')
        self.success_message = page.locator("div.status.alert-success")

    def open(self):
        self.goto("/contact_us")

    def fill_form(self, contact: ContactMessage):
        self.name_input.fill(contact.name)
        self.email_input.fill(contact.email)
        self.subject_input.fill(contact.subject)
        self.message_textarea.fill(contact.message)

    def submit(self):
        # The site shows a confirm() dialog before submitting.
        self.page.once("dialog", lambda dialog: dialog.accept())
        self.submit_button.click()
