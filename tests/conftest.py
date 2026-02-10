import os

import pytest
from dotenv import load_dotenv

load_dotenv()


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
