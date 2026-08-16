"""R10 transactional multi-region list[Op] + R2 continuation checkout."""

from __future__ import annotations

from ux_app import App, Component, Op, action, notify, update
from ux_app.drivers import effects_driver
from ux_app.html import Badge


def test_multi_region_ops_in_one_action():
    class CartBadge(Component):
        id = "cart.badge"
        count: int = 0

        def render(self):
            return Badge(self.count)

    class Rail(Component):
        id = "cart.rail"
        label: str = "idle"

        def render(self):
            return self.label

    @action("cart.add", caps=["cart.write"])
    def add(ctx):
        badge = ctx.app.runtime.components["cart.badge"]
        rail = ctx.app.runtime.components["cart.rail"]
        badge.count += 1
        rail.label = "busy"
        return [
            update("cart.badge"),
            update("cart.rail"),
            *notify("Added"),
        ]

    app = App.bind()
    app.add(CartBadge)
    app.add(Rail)
    app.html("cart.badge")
    app.html("cart.rail")
    token = app.mint("cart.add", {})
    result = app.submit("cart.add", {}, cap=token)
    assert result.ok
    pairs = [op.pair for op in result.ops]
    assert pairs.count(("ui.dom", "morph")) >= 3  # badge + rail + notices
    assert ">1<" in str(app.world.ui["cart.badge"])
    assert "busy" in str(app.world.ui["cart.rail"])


def test_checkout_follow_up_without_cap_unchanged():
    @action("checkout.start", caps=())
    def start(ctx):
        ctx.follow_up("checkout.confirm", "checkout.pay", order_id="o1")
        return [Op.kv_set("checkout.phase", "confirm")]

    @action("checkout.pay", caps=["checkout.write"])
    def pay(ctx):
        return [Op.kv_set("paid", ctx.args.get("order_id"))]

    app = App.bind()
    started = app.submit("checkout.start", {})
    assert started.ok
    cont = app.runtime.continuations["checkout.confirm"]
    assert cont.cap

    refused = app.emit("checkout.confirm")
    assert refused.kind == "authority_refusal"
    assert refused.ops == []
    assert "paid" not in app.world.kv

    ok = app.emit("checkout.confirm", cap=cont.cap)
    assert ok.ok
    assert app.world.kv["paid"] == "o1"


def test_effects_and_morph_together():
    @action("save.row", caps=())
    def save(ctx):
        from ux_app.effects import notice

        return [
            update("grid"),
            *notice("Row saved", level="success"),
        ]

    app = App.bind()
    app.use("effects", driver=effects_driver)
    result = app.submit("save.row", {})
    assert result.ok
    assert app.world.ui["notices"][-1]["text"] == "Row saved"
    assert "grid" in app.world.ui
