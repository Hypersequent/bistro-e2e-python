from typing import Literal

from playwright.sync_api import Page

from tests.schemas.models import OtherItem, OtherMenuSchema, PizzaItem, PizzaMenuSchema

Tab = Literal["pizza", "drinks", "desserts"]

GET_PIZZA_ITEMS_JS = """
() => {
    const items = Array.from(
        document.querySelectorAll('section#menu > div > div.menu--is-visible > div.row')
    );
    return items.map((item) => {
        const name = item.querySelector('h3.item__title')?.textContent || '';
        const price = item.querySelector('span.item__price')?.textContent || '';
        const description = item.querySelector('p.item__description')?.textContent || '';
        const image = item.querySelector('img')?.getAttribute('src') || '';
        return { name, image, description, price };
    });
}
"""

GET_OTHER_ITEMS_JS = """
() => {
    const items = Array.from(
        document.querySelectorAll('section#menu > div > div.menu--is-visible > div.row')
    );
    return items.map((item) => {
        const name = item.querySelector('h3.item__title')?.textContent || '';
        const price = item.querySelector('span.item__price')?.textContent || '';
        const description = item.querySelector('p.item__description')?.textContent || '';
        return { name, description, price };
    });
}
"""


class Menu:
    def __init__(self, page: Page, base_url: str) -> None:
        self.page = page
        self.base_url = base_url
        self.navbar_items = page.locator("nav ul > li")
        self.tab = page.locator("div.buttons-container")

    def goto(self) -> None:
        self.page.goto(self.base_url + "/#menu")
        self.page.wait_for_timeout(100)

    def get_navbar_items(self) -> list[dict]:
        items = self.navbar_items.all()
        assert len(items) == 3

        result = []
        for item in items:
            text = item.inner_text().strip()
            cls = item.get_attribute("class") or ""
            is_active = "active" in cls
            result.append({"text": text, "isActive": is_active})
        return result

    def get_tabs(self) -> list[dict]:
        children = self.tab.locator("a").all()
        tabs = []
        for child in children:
            text = child.inner_text().strip()
            cls = child.get_attribute("class") or ""
            is_active = "is-active" in cls
            tabs.append({"text": text, "isActive": is_active})
        return tabs

    def switch_tab(self, tab: Tab) -> None:
        self.page.locator(f"a[data-target='{tab}Menu']").click()

    def get_pizza_menu(self) -> list[PizzaItem]:
        self.switch_tab("pizza")
        items = self.page.evaluate(GET_PIZZA_ITEMS_JS)
        return PizzaMenuSchema.validate_python(items)

    def get_other_menu(self, item: Literal["drinks", "desserts"]) -> list[OtherItem]:
        self.switch_tab(item)
        items = self.page.evaluate(GET_OTHER_ITEMS_JS)
        return OtherMenuSchema.validate_python(items)

    def add_menu_item_to_cart(self, idx: int) -> None:
        item = self.page.locator(
            f"section#menu > div > div.menu--is-visible > div.row:nth-of-type({idx + 1})"
        )
        item.locator("button").click()
