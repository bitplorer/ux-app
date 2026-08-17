"""Promoted overlay macros — S-pair shape and public-API isolation."""

from __future__ import annotations

import ast
from pathlib import Path

from ux_app import close_overlay, confirm, form_result, open_overlay, select_region
from ux_app.adapters import ChannelConfirm, ChannelOverlay, ChannelSelect, SMorph
from ux_app.overlay import __all__ as overlay_all
from ux_app.overlay import bind_overlay


S_PAIRS = {
    ("kv", "set"),
    ("kv", "delete"),
    ("ui.dom", "morph"),
    ("log", "append"),
    ("ui.dom", "restore"),
}


def _assert_s_only(ops: list) -> None:
    for op in ops:
        assert op.pair in S_PAIRS, f"non-S pair: {op.fq}"


def test_open_overlay_shape():
    ops = ChannelOverlay().open("dialog", key="lot", lot_id="L1")
    _assert_s_only(ops)
    assert len(ops) == 4
    assert ops[0].payload["key"] == "ui.overlay.open"
    assert ops[0].payload["value"] is True
    assert ops[1].payload == {"key": "ui.overlay.kind", "value": "dialog"}
    assert ops[2].payload["key"] == "ui.overlay.payload"
    assert ops[2].payload["value"]["key"] == "lot"
    assert ops[2].payload["value"]["lot_id"] == "L1"
    assert ops[3].pair == ("ui.dom", "morph")
    assert ops[3].payload["target"] == "overlay"


def test_close_overlay_shape():
    ops = ChannelOverlay().close()
    _assert_s_only(ops)
    assert ops[0].payload["value"] is False
    assert ops[1].pair == ("kv", "delete")
    assert ops[2].pair == ("kv", "delete")
    assert ops[3].payload["target"] == "overlay"


def test_select_region_shape():
    ops = ChannelSelect().select("tabs:main", "billing")
    _assert_s_only(ops)
    assert ops[0].payload["key"] == "ui.select.tabs.main"
    assert ops[0].payload["value"] == "billing"
    assert ops[1].payload["target"] == "tabs:main"


def test_confirm_composes_overlay():
    ops = ChannelConfirm().ask(
        "Delete?",
        "Undo impossible.",
        confirm_action="order.delete",
        order_id="o1",
    )
    _assert_s_only(ops)
    payload = ops[2].payload["value"]
    assert payload["title"] == "Delete?"
    assert payload["confirm_action"] == "order.delete"
    assert payload["order_id"] == "o1"
    assert ops[1].payload["value"] == "confirm"


def test_package_facade_exports():
    ops = open_overlay("sheet", key="filters")
    assert ops[1].payload["value"] == "sheet"
    ops = close_overlay()
    assert ops[0].payload["value"] is False
    ops = select_region("carousel:hero", "2")
    assert ops[0].payload["value"] == "2"
    ops = confirm("Sure?", "Really.", confirm_action="x.do")
    assert ops[1].payload["value"] == "confirm"


def test_form_result():
    ops = form_result(ok=True, message="Saved")
    assert ops[0].pair == ("ui.dom", "morph")
    assert any(o.pair == ("log", "append") for o in ops)
    ops2 = form_result(ok=False, message="")
    assert len(ops2) == 1


def test_bind_overlay_injection():
    from ux_app.ops import Op
    from ux_app.adapters import default_overlay

    class Fake:
        def open(self, kind, **kw):
            return [Op.kv_set("fake", kind)]

        def close(self, **kw):
            return [Op.kv_set("fake", "closed")]

    bind_overlay(Fake())
    try:
        ops = open_overlay("dialog")
        assert ops[0].payload["value"] == "dialog"
    finally:
        bind_overlay(default_overlay)


def test_open_rejects_empty_kind():
    try:
        ChannelOverlay().open("")
        raise AssertionError("expected ValueError")
    except ValueError:
        pass


def test_smorph():
    op = SMorph().morph("cart")
    assert op.pair == ("ui.dom", "morph")
    assert op.payload["target"] == "cart"


def test_overlay_all_excludes_session_keys_and_chrome():
    assert "OVERLAY_OPEN" not in overlay_all
    assert "OVERLAY_KIND" not in overlay_all
    assert "OVERLAY_PAYLOAD" not in overlay_all
    assert "chrome" not in overlay_all
    import ux_app

    assert "OVERLAY_OPEN" not in ux_app.__all__
    assert "chrome" not in ux_app.__all__


def test_overlay_module_source_has_no_public_keys():
    src = Path(__file__).resolve().parents[1] / "src" / "ux_app" / "overlay.py"
    tree = ast.parse(src.read_text(encoding="utf-8"))
    for node in tree.body:
        if isinstance(node, ast.Assign):
            for tgt in node.targets:
                if isinstance(tgt, ast.Name) and tgt.id == "__all__":
                    names = ast.literal_eval(node.value)
                    assert "OVERLAY_OPEN" not in names
                    assert "chrome" not in names
