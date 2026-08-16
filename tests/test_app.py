from __future__ import annotations

from ux_app import App, Badge, Component
from ux_app.app import KERNEL, PREVIEW
from ux_app.ops import S_PAIRS


def test_boot_empty_page_has_scripts_in_order():
    app = App.boot(title="Empty")
    page = app.page()
    assert "<title>Empty</title>" in page
    assert KERNEL in page
    assert PREVIEW in page
    assert page.index(KERNEL) < page.index(PREVIEW)
    assert 'id="content"' in page
    assert 'data-role="peer-kernel"' in page
    assert 'data-role="preview"' in page


def test_boot_pair_set_is_s():
    app = App.boot()
    assert app.stamp == S_PAIRS
    assert app.doctor() == []


def test_bind_registers_component_and_mints_cap_on_control():
    class BadgeBox(Component):
        id = "cart.badge"
        count: int = 0

        def render(self):
            return Badge(self.count, on_click=self.add)

        def add(self, sku: str = ""):
            self.count += 1

    app = App.bind()
    app.add(BadgeBox)
    markup = app.html("cart.badge")
    assert "data-action" in markup
    assert "data-cap" in markup
    assert "data-args" in markup
    assert "0" in markup


def test_production_profile_doctor_requires_durable_and_receipts():
    app = App.bind(profile="production")
    assert app.doctor() == []
    app.runtime.caps.once.durable = False
    issues = app.doctor()
    assert any("once-store" in i for i in issues)
    app.runtime.caps.once.durable = True
    app.runtime.receipts = False
    issues = app.doctor()
    assert any("receipts" in i for i in issues)


def test_profile_does_not_grant_cap_power():
    from ux_app import action
    from ux_app.ops import Op

    @action("secret.write", caps=["admin"])
    def write(ctx):
        return [Op.kv_set("secret", 1)]

    app = App.bind(profile="production")
    result = app.submit("secret.write", {})
    assert result.kind == "authority_refusal"
    assert result.ops == []


def test_duck_type_component_without_base():
    class Loose:
        id = "loose"

        def render(self):
            return "ok"

    app = App.bind()
    app.add(Loose)
    assert app.html("loose") == "ok"


def test_explain_shape():
    app = App.bind()
    info = app.explain()
    assert "actions" in info
    assert "domains" in info
    assert "stamp" in info
    assert "drivers" in info
    assert "baseline" in info["domains"]
