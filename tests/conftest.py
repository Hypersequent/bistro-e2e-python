import os
import re

import pytest
from dotenv import load_dotenv

load_dotenv()

# Map test function names to QA Sphere-friendly display names with BD-XXX markers.
# qas-cli matches markers in the format PROJECT-SEQUENCE (e.g. BD-023).
_QAS_NAMES: dict[str, str] = {
    "test_bd023_cart_operations": "BD-023: Cart operations",
    "test_bd022_order_with_cash_payment": "BD-022: Order with cash payment",
    "test_bd055_about_page_content": "BD-055: About page content",
    "test_bd026_navbar_navigation_state": "BD-026: Navbar navigation state",
    "test_bd038_menu_tabs_and_products": "BD-038: Menu tabs and products",
    "test_bd052_welcome_banner": "BD-052: Welcome banner",
}


def pytest_itemcollected(item: pytest.Item) -> None:
    """Rewrite test node IDs so JUnit XML contains QA Sphere markers (BD-XXX)."""
    # item.name looks like "test_bd023_cart_operations[chromium]"
    base_name = re.sub(r"\[.*\]$", "", item.name)
    if base_name in _QAS_NAMES:
        suffix = item.name[len(base_name) :]  # e.g. "[chromium]"
        item._nodeid = item._nodeid.replace(item.name, _QAS_NAMES[base_name] + suffix)
        item.name = _QAS_NAMES[base_name] + suffix


@pytest.fixture(scope="session")
def demo_base_url() -> str:
    url = os.getenv("DEMO_BASE_URL", "https://hypersequent.github.io/bistro/")
    return url.rstrip("/")


@pytest.fixture()
def browser_context_args(browser_context_args: dict) -> dict:
    return {**browser_context_args, "java_script_enabled": True}


@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args: dict) -> dict:
    return {**browser_type_launch_args}
