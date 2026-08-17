"""App.attach / App.control — Channel stays behind the adapter."""
from __future__ import annotations

from ux_app import App
from ux_app.isolation import scan_imports


def test_control_without_attach_uses_in_process_cap():
    app = App.boot(title="Facade", strict=False)
    attrs = app.control("nav.go", page="shop")
    assert attrs["data_action"] == "nav.go"
    assert attrs["data_cap"]
    assert "shop" in attrs["data_args"]
    assert "data_channel_action" not in attrs


def test_attach_none_is_noop():
    app = App.boot(title="Facade", strict=False)
    assert app.region_uid == "app.root"
    app.region(lambda: "<div>slot</div>")
    assert app.attach(None) is None


def test_isolation_keeps_channel_in_adapter():
    assert scan_imports() == []


def test_app_state_none_before_attach():
    app = App.boot(title="Facade", strict=False)
    assert app.state is None
