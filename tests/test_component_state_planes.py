"""Component Session/Client fields route to live Channel state after attach."""

from __future__ import annotations

from typing import Any

import pytest

from ux_app import App, Client, Component, Session, Store, Transient
from ux_app.component import field_key
from ux_app.state import Sealed


class _FakeCell:
    def __init__(self, bag: dict[str, Any], key: str, default: Any) -> None:
        self._bag = bag
        self.key = key
        self.default = default

    def get(self, default: Any = None) -> Any:
        d = self.default if default is None else default
        return self._bag.get(self.key, d)

    def set(self, value: Any) -> Any:
        if callable(value) and not isinstance(value, type):
            cur = self._bag.get(self.key, self.default)
            value = value(cur)
        self._bag[self.key] = value
        return value


class _FakeClient:
    def __init__(self) -> None:
        self.pending: list[tuple[str, Any]] = []

    def set(self, path: str, value: Any, *, persist: bool = False) -> "_FakeClient":
        self.pending.append((path, value, persist))
        return self


class _FakeState:
    def __init__(self) -> None:
        self.data: dict[str, Any] = {}
        self.client = _FakeClient()

    def session(self, key: str, default: Any = None, *, refresh: Any = None) -> _FakeCell:
        return _FakeCell(self.data, key, default)


def test_field_key_scheme():
    from ux_app.state import FieldSpec

    spec = FieldSpec(name="slide", annotation=int, default=0, plane="session")
    assert field_key("home", "slide", spec) == "home.slide"
    assert field_key("", "slide", spec) == "component.slide"


def test_session_offline_uses_values():
    class Home(Component):
        id = "home"
        slide: int = Session(0)

        def render(self):
            return str(self.slide)

    home = Home()
    assert home.slide == 0
    home.slide = 2
    assert home.slide == 2
    assert home.is_dirty()


def test_session_live_routes_through_state():
    class Home(Component):
        id = "home"
        slide: int = Session(0)

        def render(self):
            return str(self.slide)

    app = App.boot(title="t", strict=False)
    home = app.add(Home)
    fake = _FakeState()
    app._state = fake

    assert home.slide == 0
    home.slide = 3
    assert fake.data["home.slide"] == 3
    assert home.slide == 3
    # Mirror kept for offline/SSR coherence
    assert home._values["slide"] == 3


def test_client_live_enqueues_ops():
    class Chrome(Component):
        id = "chrome"
        theme: str = Client("dark", key="ui.theme")

        def render(self):
            return self.theme

    app = App.boot(title="t", strict=False, client_state=("ui.theme", "ui.density"))
    chrome = app.add(Chrome)
    fake = _FakeState()
    app._state = fake

    assert chrome.theme == "dark"
    chrome.theme = "light"
    assert chrome.theme == "light"
    assert fake.client.pending == [("ui.theme", "light", False)]


def test_store_mirrors_world_kv():
    class Desk(Component):
        id = "desk"
        note: str = Store("")

        def render(self):
            return self.note

    app = App.boot(title="t", strict=False)
    desk = app.add(Desk)
    desk.note = "hello"
    assert desk.note == "hello"
    assert app.runtime.peer.world.kv["desk.note"] == "hello"


def test_transient_does_not_dirty_session_bag():
    class Box(Component):
        id = "box"
        flash: str = Transient("")

        def render(self):
            return self.flash

    app = App.boot(title="t", strict=False)
    box = app.add(Box)
    fake = _FakeState()
    app._state = fake
    box.flash = "x"
    assert box.flash == "x"
    assert fake.data == {}


def test_app_state_property_none_offline():
    app = App.boot(title="t", strict=False)
    assert app.state is None


def test_default_annotation_is_session_plane():
    class Box(Component):
        id = "box"
        n: int = 1

        def render(self):
            return str(self.n)

    assert Box.__ux_fields__["n"].plane == "session"
