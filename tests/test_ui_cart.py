from playwright.sync_api import Page

from tests.pageobjects.cart import Cart
from tests.pageobjects.checkout import PAYMENT_METHODS, Checkout
from tests.pageobjects.menu import Menu


def _add_to_cart(menu: Menu) -> None:
    menu.add_menu_item_to_cart(0)
    menu.add_menu_item_to_cart(1)
    menu.add_menu_item_to_cart(1)

    menu.switch_tab("drinks")
    menu.add_menu_item_to_cart(0)
    menu.add_menu_item_to_cart(1)

    menu.switch_tab("desserts")
    menu.add_menu_item_to_cart(0)


def test_bd023_cart_operations(page: Page, demo_base_url: str) -> None:
    """BD-023: User should see product list according the cart on the Checkout page.

    https://qasdemo.eu2.qasphere.com/project/BD/tcase/23
    """
    menu = Menu(page, demo_base_url)
    menu.goto()

    _add_to_cart(menu)

    pizza_menu = menu.get_pizza_menu()
    drinks_menu = menu.get_other_menu("drinks")
    desserts_menu = menu.get_other_menu("desserts")

    expected_cart = {
        "items": [
            {"name": pizza_menu[0].name, "amount": pizza_menu[0].price},
            {"name": pizza_menu[1].name, "amount": pizza_menu[1].price * 2},
            {"name": drinks_menu[0].name, "amount": drinks_menu[0].price},
            {"name": drinks_menu[1].name, "amount": drinks_menu[1].price},
            {"name": desserts_menu[0].name, "amount": desserts_menu[0].price},
        ],
        "total": (
            pizza_menu[0].price
            + pizza_menu[1].price * 2
            + drinks_menu[0].price
            + drinks_menu[1].price
            + desserts_menu[0].price
        ),
    }

    cart = Cart(page, demo_base_url)
    cart.open_cart()
    cart_response = cart.get_cart_items()
    assert cart_response.model_dump() == expected_cart

    # Remove items from cart and check response
    cart.remove_cart_item(1)
    cart.remove_cart_item(0)

    expected_cart = {
        "items": [
            {"name": drinks_menu[0].name, "amount": drinks_menu[0].price},
            {"name": drinks_menu[1].name, "amount": drinks_menu[1].price},
            {"name": desserts_menu[0].name, "amount": desserts_menu[0].price},
        ],
        "total": drinks_menu[0].price + drinks_menu[1].price + desserts_menu[0].price,
    }

    cart_response = cart.get_cart_items()
    assert cart_response.model_dump() == expected_cart

    # Add back items to cart again
    cart.close_cart()
    menu.switch_tab("pizza")
    menu.add_menu_item_to_cart(1)
    menu.add_menu_item_to_cart(1)

    cart.open_cart()
    expected_cart = {
        "items": [
            {"name": drinks_menu[0].name, "amount": drinks_menu[0].price},
            {"name": drinks_menu[1].name, "amount": drinks_menu[1].price},
            {"name": desserts_menu[0].name, "amount": desserts_menu[0].price},
            {"name": pizza_menu[1].name, "amount": pizza_menu[1].price * 2},
        ],
        "total": (
            drinks_menu[0].price
            + drinks_menu[1].price
            + desserts_menu[0].price
            + pizza_menu[1].price * 2
        ),
    }

    cart_response = cart.get_cart_items()
    assert cart_response.model_dump() == expected_cart


def test_bd022_order_with_cash_payment(page: Page, demo_base_url: str) -> None:
    """BD-022: User should place the order successfully with Cash payment.

    https://qasdemo.eu2.qasphere.com/project/BD/tcase/22
    """
    menu = Menu(page, demo_base_url)
    menu.goto()

    _add_to_cart(menu)

    pizza_menu = menu.get_pizza_menu()
    drinks_menu = menu.get_other_menu("drinks")
    desserts_menu = menu.get_other_menu("desserts")

    expected_items = {
        "items": [
            {"name": pizza_menu[0].name, "amount": pizza_menu[0].price},
            {"name": pizza_menu[1].name, "amount": pizza_menu[1].price * 2},
            {"name": drinks_menu[0].name, "amount": drinks_menu[0].price},
            {"name": drinks_menu[1].name, "amount": drinks_menu[1].price},
            {"name": desserts_menu[0].name, "amount": desserts_menu[0].price},
        ],
        "total": (
            pizza_menu[0].price
            + pizza_menu[1].price * 2
            + drinks_menu[0].price
            + drinks_menu[1].price
            + desserts_menu[0].price
        ),
    }

    cart = Cart(page, demo_base_url)
    cart.open_cart()
    page.wait_for_timeout(1000)
    cart.checkout()

    checkout = Checkout(page, demo_base_url)
    order_res = checkout.get_order_items()
    assert order_res.model_dump() == expected_items

    checkout.name_input.fill("John Doe")
    checkout.email_input.fill("johndoe@example.com")

    options = checkout.payment_method_select.locator("option").all_inner_texts()
    assert options == PAYMENT_METHODS
    checkout.payment_method_select.select_option(label="Cash on Delivery")

    checkout.place_order_button.click()
