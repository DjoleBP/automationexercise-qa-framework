from playwright.sync_api import Page

from pages.base_page import BasePage

CATEGORY_GROUPS = {
    "/category_products/1": "Women",
    "/category_products/2": "Women",
    "/category_products/7": "Women",
    "/category_products/3": "Men",
    "/category_products/6": "Men",
}


class ProductsPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.search_input = page.locator("#search_product")
        self.search_button = page.locator("#submit_search")
        self.products_title = page.get_by_role("heading", name="All Products")
        self.searched_products_title = page.get_by_role("heading", name="Searched Products")
        self.product_cards = page.locator("div.product-image-wrapper")
        self.product_names = page.locator("div.productinfo p")

    def open(self):
        self.goto("/products")

    def search_for(self, term: str):
        self.search_input.fill(term)
        self.search_button.click()

    def add_product_to_cart_by_index(self, index: int):
        self.product_cards.nth(index).locator("a.add-to-cart").first.click()

    def open_product_details_by_index(self, index: int):
        card = self.product_cards.nth(index)
        card.hover()
        card.locator("div.choose a").click()

    def go_to_category(self, category_href: str):
        group = CATEGORY_GROUPS[category_href]
        self.page.locator(f'a[href="#{group}"]').click()
        self.page.locator(f'a[href="{category_href}"]').click()

    def go_to_brand(self, brand_name: str):
        self.page.locator(f'a[href="/brand_products/{brand_name}"]').click()

    def visible_product_names(self) -> list[str]:
        return self.product_names.all_inner_texts()
