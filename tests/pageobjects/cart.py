from playwright.sync_api import Page

from tests.schemas.models import CartResponse


class Cart:
    def __init__(self, page: Page, base_url: str) -> None:
        self.page = page
        self.base_url = base_url
        self.cart_button = page.locator("div.my-cart-icon")
        self.close_cart_button = page.locator('#cart button[data-dismiss="modal"]').first
        self.checkout_button = page.locator('#cart a[href$="/checkout"]')

    def open_cart(self) -> None:
        self.cart_button.click()

    def close_cart(self) -> None:
        self.close_cart_button.click()

    def checkout(self) -> None:
        self.checkout_button.click()
        self.page.wait_for_url(self.base_url + "/checkout")

    def get_cart_items(self) -> CartResponse:
        rows = self.page.locator("#cart div.row.border-bottom").all()

        items = []
        for row in rows:
            name = row.locator("div:nth-child(2)").inner_text()
            amount = row.locator("div:nth-child(4)").inner_text()
            items.append({"name": name, "amount": amount})

        total = self.page.locator("#cart div[data-testid='cartTotal']").inner_text()

        return CartResponse.model_validate({"items": items, "total": total})

    def remove_cart_item(self, idx: int) -> None:
        rows = self.page.locator("#cart div.row.border-bottom").all()
        if idx >= len(rows):
            raise IndexError(f"Cart item with index {idx} not found")
        rows[idx].locator("button").click()
