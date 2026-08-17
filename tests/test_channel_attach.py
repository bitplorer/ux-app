"""App.attach / App.control — Channel stays behind the adapter."""
from __future__ import annotations

from ux_app import App, Component, action
from ux_app.isolation import scan_imports


def test_control_without_attach_uses_in_process_cap():
    app = App.boot(title="Facade", strict=False)
    attrs = app.control("nav.go", page="shop")
    assert attrs["data_action"] == "nav.go"
    assert attrs["data_cap"]
    assert "shop" in attrs["data_args"]
    assert "data_channel_action" not in attrs


def test_control_accepts_bound_component_method():
    class Home(Component):
        id = "home"
        slide: int = 0

        def next(self, ctx):
            self.slide = int(self.slide or 0) + 1

        def render(self):
            return str(self.slide)

    app = App.boot(title="Facade", strict=False)
    home = app.add(Home)
    attrs = app.control(home.next)
    assert attrs["data_action"] == "home.next"
    assert attrs["data_cap"]
    same = app.control("home.next")
    assert same["data_action"] == "home.next"


def test_control_accepts_action_function():
    @action("ping.x", caps=())
    def ping(ctx):
        return []

    app = App.boot(title="Facade", strict=False)
    attrs = app.control(ping)
    assert attrs["data_action"] == "ping.x"
    assert attrs["data_cap"]


def test_control_rejects_non_action():
    from ux_app.errors import DispatchError

    app = App.boot(title="Facade", strict=False)
    try:
        app.control(object())
    except DispatchError:
        return
    raise AssertionError("expected DispatchError")


def test_attach_none_is_noop():
    app = App.boot(title="Facade", strict=False)
    assert app.region_uid == "app.root"
    app.region(lambda: "<div>slot</div>")
    assert app.attach(None) is None


def test_isolation_keeps_channel_in_adapter():
    assert scan_imports() == []
