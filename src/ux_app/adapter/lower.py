"""Lower author morph onto the Channel wire form.

This module speaks Channel *shape* (``{op, target, html, morph}``) without
importing ``ux_channel``. Hosts must not copy this dict by hand.

Only ``ui.dom.morph`` is lowered here. S-pair projection (kv / log / restore)
is Channel / CEK ``project``, not a second compiler.
"""

from __future__ import annotations

from typing import Any

from ux_app.adapters import default_morph
from ux_app.ops import update


def as_selector(target: str) -> str:
    """Normalize a morph target to a CSS selector.

    ``view`` / ``#view`` / ``.tile`` / ``[data-id]`` stay unambiguous.
    Bare words become ``#id`` — the visual identity scheme, not Caps.
    """
    text = str(target).strip()
    if not text:
        raise ValueError("morph target is empty")
    if text[0] in "#.[:*":
        return text
    return f"#{text}"


def lower_morph(target: str, html: Any = "") -> dict[str, Any]:
    """``update(target, html)`` → Channel idiomorph op.

    Idiomorph is the wire strategy so matching ``id``s (especially images)
    are reused instead of remounted. The author Op stays ``ui.dom.morph``.
    """
    sel = as_selector(target)
    authored = update(sel, html)
    patch = authored.payload.get("patch")
    default_morph.morph(sel, patch)
    return {
        "op": "morph",
        "target": sel,
        "html": patch if patch is not None else html,
        "morph": "idiomorph",
    }
