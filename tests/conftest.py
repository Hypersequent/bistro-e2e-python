import os
import re

import pytest
from dotenv import load_dotenv

load_dotenv()

# QA Sphere project code. Used to detect test case markers in function names.
# e.g. test_bd023_cart_operations -> BD-023:test_bd023_cart_operations
QAS_PROJECT_CODE = "BD"

_QAS_MARKER_RE = re.compile(rf"test_({QAS_PROJECT_CODE})(\d+)_", re.IGNORECASE)


def _rewrite_qas_name(name: str) -> str:
    """Rewrite test name to include QA Sphere marker prefix.

    test_bd023_cart_operations[chromium] -> BD-023:test_bd023_cart_operations[chromium]
    """
    m = _QAS_MARKER_RE.match(name)
    if not m:
        return name
    code = m.group(1).upper()
    seq = m.group(2)
    return f"{code}-{seq}:{name}"


def pytest_itemcollected(item: pytest.Item) -> None:
    """Rewrite test node IDs so JUnit XML contains QA Sphere markers."""
    new_name = _rewrite_qas_name(item.name)
    if new_name != item.name:
        item._nodeid = item._nodeid.replace(item.name, new_name)
        item.name = new_name


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
