"""Day-1 acceptance: one file, cart increment morphs."""

from __future__ import annotations

from pathlib import Path

from ux_app import App, Badge, Component


class CartBadge(Component):
    id = "cart.badge"
    count: int = 0

    def render(self):
        return Badge(self.count, on_click=self.add)

    def add(self, sku: str = ""):
        self.count += 1


def test_click_morphs_count_zero_to_one():
    app = App.bind()
    app.add(CartBadge)
    html0 = app.html("cart.badge")
    assert "0" in html0
    assert "data-cap" in html0
    result = app.click("cart.badge")
    assert result.ok
    assert any(op.pair == ("ui.dom", "morph") for op in result.ops)
    html1 = str(app.world.ui["cart.badge"])
    assert ">1<" in html1
    assert ">0<" not in html1


def test_example_cart_is_under_40_lines_and_clean():
    path = Path(__file__).resolve().parents[1] / "examples" / "cart.py"
    text = path.read_text(encoding="utf-8")
    lines = [ln for ln in text.splitlines() if ln.strip()]
    assert len(lines) < 40
    banned = (
        "Intent",
        "CapService",
        "HTMX",
        "stamp",
        "preview",
        "chrome",
        "arm",
        "reply",
        "Effect",
        "Surface",
    )
    for word in banned:
        assert word not in text, word
