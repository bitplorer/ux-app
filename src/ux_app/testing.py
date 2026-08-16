"""Test harness helpers. Power API — not on the root __all__."""

from __future__ import annotations

from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from ux_app.app import App
    from ux_app.result import Result


def new_app(**kwargs: Any) -> "App":
    from ux_app.app import App

    return App.bind(**kwargs)


def click(app: "App", ident: str, method: str | None = None, **args: Any) -> "Result":
    return app.click(ident, method, **args)
