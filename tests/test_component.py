"""C-pre-08 — honor a foreign Component; do not wrap twice."""

from __future__ import annotations

from ux_app import App, Component
from ux_app.component import is_component


def test_foreign_reactive_init_chain_is_not_rewrapped():
    calls: list[str] = []

    class Foreign:
        def __init_subclass__(cls, **kwargs):
            super().__init_subclass__(**kwargs)
            calls.append(cls.__name__)
            cls._ensure_init_chain = True  # type: ignore[attr-defined]

        def _ensure_init_chain(self) -> None:  # pragma: no cover - marker
            return None

    class BadgeLike(Foreign):
        id = "foreign"
        n: int = 0

        def render(self):
            return str(self.n)

    assert BadgeLike._ensure_init_chain is True
    assert is_component(BadgeLike())
    app = App.bind()
    app.add(BadgeLike)
    assert app.html("foreign") == "0"
    # We never inherited Component, so we did not run a second init chain.
    assert Component not in BadgeLike.__mro__


def test_optional_base_collects_fields_once():
    class Box(Component):
        id = "box"
        n: int = 1

        def render(self):
            return str(self.n)

    assert "n" in Box.__ux_fields__
    assert Box.__ux_fields__["n"].plane == "session"
