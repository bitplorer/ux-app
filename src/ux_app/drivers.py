"""Bundled Peer drivers. Apply only — no mint, no Channel import."""

from __future__ import annotations

from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from ux_app.ops import Op


def search_driver(op: "Op", world: Any) -> None:
    """Apply search.hits / search.clear onto world.ui[target]."""
    target = op.payload.get("target")
    if not target:
        raise ValueError("search op missing target")
    if op.name == "clear":
        world.ui[str(target)] = {"items": [], "q": ""}
        return
    world.ui[str(target)] = {
        "items": list(op.payload.get("items") or []),
        "q": op.payload.get("q") or "",
    }
