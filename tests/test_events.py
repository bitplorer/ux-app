from __future__ import annotations

from ux_app import App, Op, action
from ux_app.ops import store_set


def test_follow_up_requires_host_cap():
    @action("search.type", caps=())
    def search_type(ctx):
        q = ctx.args.get("q") or ""
        ctx.follow_up(
            "input.idle:search",
            "search.commit",
            args_from={"q": "search.pending"},
        )
        return [store_set("search.pending", q)]

    @action("search.commit", caps=["search.read"])
    def search_commit(ctx):
        return [
            Op(
                "search",
                "hits",
                {"target": "results", "items": [ctx.args["q"]], "q": ctx.args["q"]},
            )
        ]

    app = App.bind()
    from ux_app.drivers import search_driver

    app.use("search", driver=search_driver)
    typed = app.submit("search.type", {"q": "widget"})
    assert typed.ok
    cont = app.runtime.continuations["input.idle:search"]
    assert cont.cap

    refused = app.emit("input.idle:search", {"search.pending": "widget"})
    assert refused.kind == "authority_refusal"
    assert refused.ops == []
    assert "results" not in app.world.ui

    ok = app.emit("input.idle:search", {"search.pending": "widget"}, cap=cont.cap)
    assert ok.ok
    assert app.world.ui["results"]["items"] == ["widget"]


def test_peer_runtime_has_no_mint():
    app = App.bind()
    assert not hasattr(app.runtime.peer, "mint")
    assert not callable(getattr(app.runtime.peer, "mint", None))
