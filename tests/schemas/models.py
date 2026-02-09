import re
from typing import Annotated

from pydantic import BaseModel, BeforeValidator, TypeAdapter


def parse_price(value: object) -> int:
    if isinstance(value, int):
        return value
    if isinstance(value, str):
        match = re.fullmatch(r"\$(\d+)", value)
        if match:
            return int(match.group(1))
    raise ValueError(f"Invalid price format: {value!r}")


Price = Annotated[int, BeforeValidator(parse_price)]


class PizzaItem(BaseModel):
    name: str
    image: str
    description: str
    price: Price


class OtherItem(BaseModel):
    name: str
    description: str
    price: Price


class CartItem(BaseModel):
    name: str
    amount: Price


class CartResponse(BaseModel):
    items: list[CartItem]
    total: Price


PizzaMenuSchema = TypeAdapter(list[PizzaItem])
OtherMenuSchema = TypeAdapter(list[OtherItem])
