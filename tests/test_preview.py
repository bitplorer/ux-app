from __future__ import annotations

from ux_app import App, Op, action, preview


def test_preview_does_not_write_authority_kv():
    app = App.bind()
    before = dict(app.world.kv)
    preview.pending("results", True)
    preview.update("hdr", {"text": "…"})
    preview.filter("search:hits", "q", "results")
    assert app.world.kv == before
    assert "results" not in app.world.kv


def test_preview_cleared_after_result():
    @action("touch", caps=())
    def touch(ctx):
        return [Op.kv_set("k", 1)]

    app = App.bind()
    preview.pending("results", True)
    preview.update("hdr", {"text": "soon"})
    assert not preview.is_empty()
    result = app.submit("touch", {})
    assert result.ok
    assert preview.is_empty()


def test_preview_not_an_op_return():
    @action("bad", caps=())
    def bad(ctx):
        return [preview.pending("results", True)]

    app = App.bind()
    result = app.submit("bad", {})
    assert result.kind == "dispatch_error"
    assert "preview" in (result.error or "")
