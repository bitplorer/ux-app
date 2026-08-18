"""adapter.lower — author morph → Channel idiomorph. No Channel import."""

from __future__ import annotations

import pytest

from ux_app.adapter import as_selector, lower_morph
from ux_app.ops import update


def test_as_selector_bare_word_becomes_id():
    assert as_selector("view") == "#view"
    assert as_selector("  view  ") == "#view"


def test_as_selector_keeps_css():
    assert as_selector("#view") == "#view"
    assert as_selector(".tile") == ".tile"
    assert as_selector("[data-sku]") == "[data-sku]"


def test_as_selector_empty_raises():
    with pytest.raises(ValueError, match="empty"):
        as_selector("  ")


def test_lower_morph_uses_update_and_idiomorph():
    html = "<section id='view'>ok</section>"
    authored = update("#view", html)
    wire = lower_morph("view", html)
    assert wire["op"] == "morph"
    assert wire["target"] == "#view"
    assert wire["morph"] == "idiomorph"
    assert wire["html"] == authored.payload.get("patch")
