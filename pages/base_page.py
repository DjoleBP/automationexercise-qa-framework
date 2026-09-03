from playwright.sync_api import Page

from utils.config import BASE_URL


class BasePage:
    def __init__(self, page: Page):
        self.page = page

    def goto(self, path: str = "/"):
        self.page.goto(f"{BASE_URL}{path}")

    def title(self) -> str:
        return self.page.title()
