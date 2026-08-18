"""adapter.compose — fold + XOR law. No Channel import."""

from __future__ import annotations

import pytest

from ux_app.adapter import ComposeConflict, compose, lower_morph
from ux_app.ops import Op, update


class _Scene:
    def __init__(self, ops):
        self._ops = ops

    def play(self):
        return {"ok": True, "ops": list(self._ops)}


def test_folds_dicts_and_skips_none():
    ops = compose(
        {"op": "morph", "target": "#a", "html": "1", "morph": "idiomorph"},
        None,
        {"op": "set_attr", "target": "#a", "attrs": {"hidden": None}},
    )
    assert [op["op"] for op in ops] == ["morph", "set_attr"]


def test_lowers_update_op():
    authored = update("view", "<p>x</p>")
    ops = compose(authored)
    assert ops == [lower_morph("view", "<p>x</p>")]
    assert ops[0]["morph"] == "idiomorph"
    assert ops[0]["target"] == "#view"


def test_rejects_non_morph_op():
    with pytest.raises(TypeError, match="ui.dom.morph"):
        compose(Op.kv_set("k", 1))


def test_folds_scene_play():
    scene = _Scene([{"op": "transition.play", "plan": {"kind": "plan"}}])
    ops = compose(scene)
    assert ops[0]["op"] == "transition.play"


def test_navigate_ordered_last():
    ops = compose(
        {"op": "navigate", "href": "/shop"},
        {"op": "morph", "target": "#view", "html": "<p/>", "morph": "idiomorph"},
    )
    assert [op["op"] for op in ops] == ["morph", "navigate"]


def test_xor_morph_and_motion_html():
    scene = _Scene(
        [
            {
                "op": "transition.play",
                "plan": {
                    "kind": "plan",
                    "root": {
                        "kind": "track",
                        "target": "#view",
                        "html": "<section id='view'>x</section>",
                    },
                },
            }
        ]
    )
    with pytest.raises(ComposeConflict, match="XOR"):
        compose(
            {"op": "morph", "target": "view", "html": "<section/>", "morph": "idiomorph"},
            scene,
        )


def test_motion_without_html_may_share_target():
    scene = _Scene(
        [
            {
                "op": "transition.play",
                "plan": {
                    "kind": "plan",
                    "root": {"kind": "track", "target": "#view", "role": "enter"},
                },
            }
        ]
    )
    ops = compose(
        {"op": "morph", "target": "#view", "html": "<section/>", "morph": "idiomorph"},
        scene,
    )
    assert len(ops) == 2
