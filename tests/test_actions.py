from __future__ import annotations

import pytest

from ux_app import App, Component, Op, action
from ux_app.action import ActionSpec, validate_args
from ux_app.errors import ValidationError


def test_caps_required_on_decorator():
    with pytest.raises(TypeError, match="requires caps"):

        @action("orders.create")
        def create(ctx):
            return []


def test_public_opt_out_is_explicit():
    @action("ping", caps=())
    def ping(ctx):
        return []

    assert ping.__ux_action__.public is True


def test_cap_refuse_empty_ops_world_unchanged():
    @action("inc", caps=["orders.write"])
    def inc(ctx):
        return [Op.kv_set("n", 1)]

    app = App.bind()
    before = dict(app.world.kv)
    result = app.submit("inc", {})
    assert result.kind == "authority_refusal"
    assert result.ops == []
    assert result.ok is False
    assert app.world.kv == before


def test_present_bogus_cap_on_public_still_verifies():
    class C(Component):
        id = "c"
        n: int = 0

        def render(self):
            return str(self.n)

        def bump(self):
            self.n += 1

    app = App.bind()
    app.add(C)
    before = dict(app.world.ui)
    result = app.submit("c.bump", {}, cap="not-a-real-cap")
    assert result.kind == "authority_refusal"
    assert result.ops == []
    assert app.world.ui == before


def test_once_store_down_refuses():
    @action("go", caps=["x"])
    def go_fn(ctx):
        return [Op.kv_set("ran", True)]

    app = App.bind()
    token = app.mint("go", {})
    app.runtime.caps.once.down = True
    result = app.submit("go", {}, cap=token)
    assert result.kind == "authority_refusal"
    assert result.ops == []
    assert "ran" not in app.world.kv


def test_cap_reuse_refuses():
    @action("oncey", caps=["x"])
    def oncey(ctx):
        return [Op.kv_set("n", 1)]

    app = App.bind()
    token = app.mint("oncey", {})
    first = app.submit("oncey", {}, cap=token)
    assert first.ok
    second = app.submit("oncey", {}, cap=token)
    assert second.kind == "authority_refusal"
    assert second.ops == []


def test_sealed_qty_arg_no_coerce():
    @action("buy", caps=["x"])
    def buy(ctx, qty: int):
        return [Op.kv_set("qty", qty)]

    spec = buy.__ux_action__
    with pytest.raises(ValidationError, match="no coerce"):
        validate_args(spec, {"qty": "1"})

    app = App.bind()
    token = app.mint("buy", {"qty": "1"})
    result = app.submit("buy", {"qty": "1"}, cap=token)
    assert result.kind == "validation"
    assert result.ok is False
    assert "qty" not in app.world.kv


@pytest.mark.asyncio
async def test_async_action_sync_refuses_async_runs():
    @action("slow", caps=())
    async def slow(ctx):
        return [Op.kv_set("done", True)]

    app = App.bind()
    sync = app.submit("slow", {})
    assert sync.kind == "dispatch_error"
    assert "async" in (sync.error or "")
    assert "done" not in app.world.kv
    result = await app.async_submit("slow", {})
    assert result.ok
    assert app.world.kv["done"] is True


def test_none_return_on_component_method_updates():
    class Box(Component):
        id = "box"
        n: int = 0

        def render(self):
            return str(self.n)

        def inc(self):
            self.n += 1

    app = App.bind()
    app.add(Box)
    app.html("box")
    result = app.click("box", "inc")
    assert result.ok
    assert any(op.pair == ("ui.dom", "morph") for op in result.ops)
    assert "1" in str(app.world.ui["box"])
