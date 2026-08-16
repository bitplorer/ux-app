from __future__ import annotations

from ux_app import App
from ux_app.doctor import PRODUCTION
from ux_app.ui_health import COMPOSITE_RUNTIMES, doctor_ui_health


def test_ui_profile_does_not_fail_undeclared_runtime():
    app = App.bind()
    app.require_composite("carousel", "dialog")
    assert doctor_ui_health(app) == []
    assert app.doctor() == []


def test_production_fails_undeclared_alpine():
    app = App.bind(profile="production")
    app.require_composite("carousel")
    issues = app.doctor()
    assert any("undeclared runtime 'alpine'" in i for i in issues)


def test_production_passes_when_declared():
    app = App.bind(profile="production")
    app.require_composite("carousel", "dialog", "tabs")
    app.declare_runtime("alpine")
    issues = [i for i in app.doctor() if "undeclared runtime" in i]
    assert issues == []


def test_pure_html_composites_need_no_runtime():
    app = App.bind(profile="production")
    app.require_composite("slider", "chart", "toast", "datepicker")
    issues = [i for i in app.doctor() if "undeclared runtime" in i]
    assert issues == []


def test_composite_map_covers_battery():
    for stem in ("carousel", "dialog", "tabs", "slider", "chart", "toast"):
        assert stem in COMPOSITE_RUNTIMES
    assert "production" in PRODUCTION
