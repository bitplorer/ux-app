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


def test_field_key_scheme():
    from ux_app.component import field_key
    from ux_app.state import Session, Store, Transient

    class Home(Component):
        id = "home"
        slide: int = Session(0)
        note: str = Store("")
        flash: str = Transient("")
        theme: str = Client("dark", key="ui.theme")

        def render(self):
            return str(self.slide)

    h = Home()
    assert field_key(h, "slide") == "home.slide"
    assert field_key(h, "note") == "home.note"
    assert field_key(h, "flash") == "home.flash"
    assert field_key(h, "theme") == "ui.theme"
    assert h.field_key("slide") == "home.slide"


def test_session_field_offline_is_plain_value():
    from ux_app.state import Session

    class Home(Component):
        id = "home"
        slide: int = Session(0)

        def render(self):
            return str(self.slide)

    app = App.bind()
    home = app.add(Home)
    assert home.slide == 0
    home.slide = 2
    assert home.slide == 2
    assert home.is_dirty()
    assert app.state is None


def test_store_field_mirrors_world_kv():
    from ux_app.state import Store

    class Desk(Component):
        id = "desk"
        label: str = Store("a")

        def render(self):
            return self.label

    app = App.bind()
    desk = app.add(Desk)
    desk.label = "b"
    assert desk.label == "b"
    assert app.runtime.peer.world.kv.get("desk.label") == "b"
