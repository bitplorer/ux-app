from __future__ import annotations

import pytest

from ux_app import App, Client, Component, Sealed
from ux_app.errors import ValidationError
from ux_app.state import collect_fields, is_money_shaped


def test_default_plane_is_session():
    class Box(Component):
        id = "box"
        count: int = 0

        def render(self):
            return str(self.count)

    specs = collect_fields(Box)
    assert specs["count"].plane == "session"


def test_client_key_not_on_allowlist_raises():
    class Theme(Component):
        id = "theme"
        accent: str = Client("blue", key="ui.accent")

        def render(self):
            return self.accent

    app = App.bind()
    with pytest.raises(ValidationError, match="allowlist"):
        app.add(Theme)


def test_money_shaped_client_fails_type_gate():
    assert is_money_shaped("price")
    assert is_money_shaped("qty")
    assert is_money_shaped("role")

    class Priced(Component):
        id = "priced"
        price: int = Client(0, key="ui.theme")

        def render(self):
            return str(self.price)

    app = App.bind()
    with pytest.raises(ValidationError, match="money-shaped"):
        app.add(Priced)


def test_sealed_int_no_coerce():
    class Item(Component):
        id = "item"
        qty: int = Sealed(0)

        def render(self):
            return str(self.qty)

    item = Item()
    with pytest.raises(ValidationError, match="no coerce"):
        item.qty = "1"
    item.qty = 2
    assert item.qty == 2


def test_sealed_init_kwargs_no_coerce():
    class Item(Component):
        id = "item"
        qty: int = Sealed(0)

        def render(self):
            return str(self.qty)

    with pytest.raises(ValidationError, match="no coerce"):
        Item(qty="1")
