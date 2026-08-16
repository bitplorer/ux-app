"""Effects DomainPack helpers. Apply only — no mint, no Channel import.

notify() stays S-only (log.append + ui.dom.morph notices). Rich notices
use this pack after ``app.use("effects", driver=effects_driver)``.
"""

from __future__ import annotations

import html
from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from ux_app.ops import Op


def notice(text: str, *, level: str = "info", target: str = "notices") -> list["Op"]:
    """Stamped ui.notice.push. Legal only after effects is on the stamp."""
    from ux_app.ops import Op

    safe = html.escape(str(text))
    return [
        Op("ui.notice", "push", {"target": target, "text": safe, "level": level}),
    ]


def clear_notices(target: str = "notices") -> "Op":
    from ux_app.ops import Op

    return Op("ui.notice", "clear", {"target": target})


def effects_driver(op: "Op", world: Any) -> None:
    """Apply ui.notice.push / ui.notice.clear onto world.ui[target]."""
    target = str(op.payload.get("target") or "notices")
    if op.name == "clear":
        world.ui[target] = []
        return
    items = list(world.ui.get(target) or [])
    if not isinstance(items, list):
        items = []
    items.append(
        {
            "text": op.payload.get("text") or "",
            "level": op.payload.get("level") or "info",
        }
    )
    world.ui[target] = items
