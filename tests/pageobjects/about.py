from playwright.sync_api import Page


class About:
    def __init__(self, page: Page, base_url: str) -> None:
        self.page = page
        self.base_url = base_url
        self.heading = page.locator("h1")
        self.body = page.locator("article")
        self.navbar_items = page.locator("nav ul > li")

    def goto(self) -> None:
        self.page.goto(self.base_url + "/about")

    def get_heading(self) -> str:
        return self.heading.inner_text().strip()

    def get_body(self) -> str:
        return self.body.inner_text().strip()

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
