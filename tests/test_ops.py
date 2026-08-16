from __future__ import annotations

import pytest

from ux_app.errors import IllegalOp
from ux_app.ops import S_PAIRS, Op, as_ops, check_stamp, go, notify, update, validate_pair
from ux_app.preview import preview


def test_s_pairs_are_the_five():
    assert S_PAIRS == {
        ("kv", "set"),
        ("kv", "delete"),
        ("log", "append"),
        ("ui.dom", "morph"),
        ("ui.dom", "restore"),
    }


def test_pair_identity_legal():
    op = Op("ui.dom", "morph", {"target": "x"})
    assert op.pair == ("ui.dom", "morph")


def test_pair_identity_split_alias_illegal():
    with pytest.raises(IllegalOp, match="must not contain dots"):
        Op("ui", "dom.morph", {"target": "x"})


def test_forbidden_ns_prefix():
    with pytest.raises(IllegalOp):
        validate_pair("cek.secret", "x")
    with pytest.raises(IllegalOp):
        validate_pair("sys.host", "x")
    with pytest.raises(IllegalOp):
        validate_pair("_hidden", "x")


def test_too_many_dots_in_ns():
    with pytest.raises(IllegalOp, match="too many dots"):
        validate_pair("a.b.c.d", "x")


def test_notify_and_go_expand_to_s_only():
    for op in notify("<b>hi</b>"):
        assert op.pair in S_PAIRS
    for op in go("/orders/1"):
        assert op.pair in S_PAIRS
    assert all(op.fq != "ui.toast" and op.pair != ("ui", "toast") for op in notify("x"))
    assert all(op.pair != ("nav", "push") for op in go("/x"))


def test_notify_escapes_html():
    ops = notify("<script>alert(1)</script>")
    joined = " ".join(str(op.payload) for op in ops)
    assert "<script>" not in joined
    assert "lt;script" in joined


def test_update_is_morph():
    op = update("cart.badge")
    assert op.pair == ("ui.dom", "morph")
    assert op.payload["target"] == "cart.badge"


def test_preview_is_illegal_inside_ops():
    with pytest.raises(IllegalOp, match="preview is not an Op"):
        as_ops([preview.pending("results", True)])


def test_check_stamp_rejects_undeclared():
    op = Op("nav", "push", {"to": "/"})
    with pytest.raises(IllegalOp, match="absent from session stamp"):
        check_stamp([op], S_PAIRS)


def test_stamped_constructor_enforces_stamp():
    with pytest.raises(IllegalOp):
        Op.stamped("search", "hits", {}, S_PAIRS)
