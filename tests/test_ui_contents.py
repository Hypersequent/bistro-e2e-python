from playwright.sync_api import Page

from tests.pageobjects.about import About
from tests.pageobjects.menu import Menu
from tests.pageobjects.welcome import Welcome


def test_bd055_about_page_content(page: Page, demo_base_url: str) -> None:
    """BD-055: User should see the content according to the About Us information.

    https://qasdemo.eu2.qasphere.com/project/BD/tcase/55
    """
    about = About(page, demo_base_url)
    about.goto()

    assert about.get_heading() == "Welcome to Bistro Delivery"
    assert (
        "So, while you won't actually be able to order your favorite quiche or ratatouille from us,"
        " you can certainly rely on QA Sphere to deliver the tools and systems you need to ensure"
        " your software projects are a recipe for success. Bon appétit and happy testing!"
    ) in about.get_body()


def test_bd026_navbar_navigation_state(page: Page, demo_base_url: str) -> None:
    """BD-026: Correct display of blocks and buttons in the navbar.

    https://qasdemo.eu2.qasphere.com/project/BD/tcase/26
    """
    welcome = Welcome(page, demo_base_url)
    about = About(page, demo_base_url)
    menu = Menu(page, demo_base_url)

    welcome.goto()
    navbar_items = welcome.get_navbar_items()
    assert navbar_items == [
        {"text": "Welcome", "isActive": True},
        {"text": "Today's Menu", "isActive": False},
        {"text": "About us", "isActive": False},
    ]

    menu.goto()
    navbar_items = menu.get_navbar_items()
    assert navbar_items == [
        {"text": "Welcome", "isActive": False},
        {"text": "Today's Menu", "isActive": True},
        {"text": "About us", "isActive": False},
    ]

    about.goto()
    navbar_items = about.get_navbar_items()
    assert navbar_items == [
        {"text": "Welcome", "isActive": False},
        {"text": "Today's Menu", "isActive": False},
        {"text": "About us", "isActive": True},
    ]


def test_bd038_menu_tabs_and_products(page: Page, demo_base_url: str) -> None:
    """BD-038: User should see the Pizzas list by default on the Todays Menu block.

    https://qasdemo.eu2.qasphere.com/project/BD/tcase/38
    """
    menu = Menu(page, demo_base_url)
    menu.goto()

    pizza_menu = menu.get_pizza_menu()
    tabs = menu.get_tabs()
    assert tabs == [
        {"text": "PIZZAS", "isActive": True},
        {"text": "DRINKS", "isActive": False},
        {"text": "DESSERTS", "isActive": False},
    ]
    assert len(pizza_menu) > 0

    drinks_menu = menu.get_other_menu("drinks")
    tabs = menu.get_tabs()
    assert tabs == [
        {"text": "PIZZAS", "isActive": False},
        {"text": "DRINKS", "isActive": True},
        {"text": "DESSERTS", "isActive": False},
    ]
    assert len(drinks_menu) > 0

    desserts_menu = menu.get_other_menu("desserts")
    tabs = menu.get_tabs()
    assert tabs == [
        {"text": "PIZZAS", "isActive": False},
        {"text": "DRINKS", "isActive": False},
        {"text": "DESSERTS", "isActive": True},
    ]
    assert len(desserts_menu) > 0


def test_bd052_welcome_banner(page: Page, demo_base_url: str) -> None:
    """BD-052: User should see the Todays Menu block after clicking the button in Welcome banner.

    https://qasdemo.eu2.qasphere.com/project/BD/tcase/52
    """
    welcome = Welcome(page, demo_base_url)
    welcome.goto()

    assert welcome.get_heading() == "Bistro Delivery"
    assert welcome.get_body() == (
        "Elegance of French&Italian Cuisine Delivered Directly to Your Doorstep!"
    )
    assert welcome.get_goto_menu_button() == "View Today's Menu"
