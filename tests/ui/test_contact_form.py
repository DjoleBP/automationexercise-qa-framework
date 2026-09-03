import pytest

from pages.contact_us_page import ContactUsPage
from pages.home_page import HomePage
from utils.data_factory import ContactMessage, unique_email


@pytest.mark.smoke
def test_submit_contact_form_with_valid_data(page):
    contact_page = ContactUsPage(page)
    contact_page.open()
    contact_page.fill_form(ContactMessage())
    contact_page.submit()

    assert contact_page.success_message.is_visible()


@pytest.mark.negative
def test_submit_contact_form_with_required_fields_empty(page):
    contact_page = ContactUsPage(page)
    contact_page.open()
    contact_page.submit()

    assert not contact_page.success_message.is_visible()
    assert contact_page.page.url.endswith("/contact_us")


@pytest.mark.smoke
def test_subscribe_to_newsletter(page):
    home = HomePage(page)
    home.open()
    home.subscribe_to_newsletter(unique_email("newsletter"))

    assert home.subscribe_success_message.is_visible()
