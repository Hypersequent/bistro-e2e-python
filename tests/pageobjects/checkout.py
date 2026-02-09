import time

from playwright.sync_api import Page

from tests.schemas.models import CartResponse

PAYMENT_METHODS = ["Cash on Delivery", "Card Payment on Delivery"]


class Checkout:
    def __init__(self, page: Page, base_url: str) -> None:
        self.page = page
        self.base_url = base_url
        self.name_input = page.locator("#customerName")
        self.email_input = page.locator("#customerAddress")
        self.payment_method_select = page.locator("#paymentMethod")
        self.place_order_button = page.locator('form button[type="submit"]')

    def get_order_items(self) -> CartResponse:
        assert self.page.url == self.base_url + "/checkout"
        time.sleep(0.5)

        rows = self.page.locator("table > tbody > tr").all()

        items = []
        for row in rows[:-1]:
            name = row.locator("td:nth-child(2)").inner_text()
            amount = row.locator("td:nth-child(4)").inner_text()
            items.append({"name": name, "amount": amount})

        total = self.page.locator(
            "table.table > tbody > tr:last-of-type td:nth-child(4)"
        ).inner_text()

        return CartResponse.model_validate({"items": items, "total": total})
