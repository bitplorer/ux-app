"""R3 perception-native search: preview.filter then commit Action."""

from __future__ import annotations

from ux_app import App, Op, action, preview
from ux_app.drivers import search_driver


def test_preview_then_commit():
    @action("catalog.type", caps=())
    def typeahead(ctx):
        q = ctx.args.get("q") or ""
        preview.filter("search:hits", q, "results")
        preview.pending("results", True)
        return [Op.kv_set("search.pending", q)]

    @action("catalog.commit", caps=())
    def commit(ctx):
        q = ctx.args.get("q") or ""
        return [
            Op(
                "search",
                "hits",
                {"target": "results", "items": [f"hit:{q}"], "q": q},
            )
        ]

    app = App.bind()
    app.use("search", driver=search_driver)

    preview.filter("search:hits", "wid", "results")
    assert "results" not in app.world.kv
    assert preview.filters["results"]["q"] == "wid"

    typed = app.submit("catalog.type", {"q": "widget"})
    assert typed.ok
    assert preview.is_empty()  # Result clears preview
    assert app.world.kv["search.pending"] == "widget"

    committed = app.submit("catalog.commit", {"q": "widget"})
    assert committed.ok
    assert app.world.ui["results"]["items"] == ["hit:widget"]
    assert preview.is_empty()


def test_preview_returned_from_action_is_illegal():
    @action("catalog.bad", caps=())
    def bad(ctx):
        return [preview.filter("search:hits", "q", "results")]

    app = App.bind()
    result = app.submit("catalog.bad", {})
    assert result.kind == "dispatch_error"
    assert "preview" in (result.error or "")
    assert result.ops == []
