from __future__ import annotations

import pytest

from ux_app import App, Op, action, notify
from ux_app.effects import clear_notices, effects_driver, notice
from ux_app.errors import IllegalOp
from ux_app.ops import S_PAIRS


def test_notify_still_s_only():
    for op in notify("hello"):
        assert op.pair in S_PAIRS
    assert all(op.pair != ("ui.notice", "push") for op in notify("x"))


def test_effects_without_driver_fails_doctor():
    app = App.bind()
    app.use("effects")
    issues = app.doctor()
    assert any("ui.notice.push" in i and "no driver" in i for i in issues)


def test_effects_with_driver_applies():
    @action("orders.save", caps=())
    def save(ctx):
        return notice("Saved", level="success")

    app = App.bind()
    app.use("effects", driver=effects_driver)
    assert app.doctor() == []
    result = app.submit("orders.save", {})
    assert result.ok
    assert app.world.ui["notices"] == [{"text": "Saved", "level": "success"}]


def test_effects_refuse_undeclared_leaves_world():
    @action("orders.ping", caps=())
    def ping(ctx):
        return notice("nope")

    app = App.bind()
    before = dict(app.world.ui)
    result = app.submit("orders.ping", {})
    assert result.kind == "dispatch_error"
    assert result.ops == []
    assert app.world.ui == before


def test_clear_notices():
    @action("notices.wipe", caps=())
    def wipe(ctx):
        return [clear_notices()]

    app = App.bind()
    app.use("effects", driver=effects_driver)
    app.world.ui["notices"] = [{"text": "old", "level": "info"}]
    result = app.submit("notices.wipe", {})
    assert result.ok
    assert app.world.ui["notices"] == []


def test_notice_escapes_html():
    ops = notice("<script>x</script>")
    joined = " ".join(str(op.payload) for op in ops)
    assert "<script>" not in joined
