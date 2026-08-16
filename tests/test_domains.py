from __future__ import annotations

import pytest

from ux_app import App, Op, action
from ux_app.domains import DomainTable
from ux_app.drivers import search_driver
from ux_app.errors import IllegalOp


def test_use_search_without_driver_fails_doctor():
    app = App.bind()
    app.use("search")
    issues = app.doctor()
    assert any("search.hits" in i and "no driver" in i for i in issues)


def test_use_search_with_driver_applies():
    @action("search.run", caps=())
    def run(ctx):
        return [Op("search", "hits", {"target": "results", "items": ["a"], "q": "a"})]

    app = App.bind()
    app.use("search", driver=search_driver)
    assert app.doctor() == []
    result = app.submit("search.run", {})
    assert result.ok
    assert app.world.ui["results"]["items"] == ["a"]


def test_product_domain_illegal_before_register():
    @action("orders.mark", caps=())
    def mark(ctx):
        return [Op("orders", "status", {"target": "panel", "state": "open"})]

    app = App.bind()
    result = app.submit("orders.mark", {})
    assert result.kind == "dispatch_error"
    assert "orders.status" in (result.error or "")
    assert "panel" not in app.world.ui


def test_product_domain_with_driver_applies():
    def orders_driver(op, world):
        world.ui[str(op.payload["target"])] = op.payload["state"]

    @action("orders.mark", caps=())
    def mark(ctx):
        return [Op("orders", "status", {"target": "panel", "state": "open"})]

    app = App.bind()
    app.domain("orders", "1.0.0", [("orders", "status")], driver=orders_driver)
    result = app.submit("orders.mark", {})
    assert result.ok
    assert app.world.ui["panel"] == "open"


def test_cannot_overwrite_core_stdlib():
    app = App.bind()
    with pytest.raises(IllegalOp, match="cannot overwrite core"):
        app.domain("baseline", "2.0.0", [("kv", "set")])


def test_empty_seed_pairs_illegal():
    app = App.bind()
    with pytest.raises(IllegalOp, match="no seed pairs"):
        app.domain("empty", "1.0.0", [])


def test_cek_off_still_has_pair_set_and_refuses_undeclared():
    @action("nav.go", caps=())
    def nav_go(ctx):
        return [Op("nav", "push", {"to": "/"})]

    app = App.boot(title="x", cek="off")
    assert ("ui.dom", "morph") in app.stamp
    result = app.submit("nav.go", {})
    assert result.kind == "dispatch_error"
    assert result.ops == []


def test_domain_table_undriven_tracks_search():
    table = DomainTable()
    table.use("search")
    assert ("search", "hits") in table.undriven()
    table.register_driver("search", "hits", search_driver)
    table.register_driver("search", "clear", search_driver)
    assert table.undriven() == []
