# Copyright (c) 2026 ux-app
"""Default Channel adapters for design-system ports.

All session key names and morph defaults live here.
Swap or subclass these without touching macros or product Actions.
"""

from __future__ import annotations

from typing import Any

from ux_app.ops import Op
from ux_app.ports import ConfirmPort, MorphPort, OverlayPort, SelectPort, TokenPort

__all__ = [
    "SMorph",
    "ChannelOverlay",
    "ChannelSelect",
    "ChannelConfirm",
    "TableTokens",
    "form_result",
    "default_morph",
    "default_overlay",
    "default_select",
    "default_confirm",
    "default_tokens",
    "OVERLAY_OPEN",
    "OVERLAY_KIND",
    "OVERLAY_PAYLOAD",
    "SELECT_PREFIX",
]

# ── Session key scheme (change ONLY here if the scheme evolves) ─────────────
OVERLAY_OPEN = "ui.overlay.open"
OVERLAY_KIND = "ui.overlay.kind"
OVERLAY_PAYLOAD = "ui.overlay.payload"
SELECT_PREFIX = "ui.select."


class SMorph:
    """MorphPort → S pair ui.dom.morph."""

    def morph(self, target: str, patch: Any = None) -> Op:
        return Op.ui_morph(target, patch)


class ChannelOverlay:
    """OverlayPort → session cells + morph (one overlay cell)."""

    def __init__(self, morph: MorphPort | None = None) -> None:
        self._morph = morph or SMorph()

    def open(
        self,
        kind: str,
        *,
        key: str | None = None,
        target: str = "overlay",
        **payload: Any,
    ) -> list[Op]:
        if not kind or not isinstance(kind, str):
            raise ValueError("overlay kind must be a non-empty str")
        body: dict[str, Any] = dict(payload)
        if key is not None:
            body["key"] = key
        return [
            Op.kv_set(OVERLAY_OPEN, True),
            Op.kv_set(OVERLAY_KIND, kind),
            Op.kv_set(OVERLAY_PAYLOAD, body),
            self._morph.morph(target),
        ]

    def close(self, *, target: str = "overlay") -> list[Op]:
        return [
            Op.kv_set(OVERLAY_OPEN, False),
            Op.kv_delete(OVERLAY_KIND),
            Op.kv_delete(OVERLAY_PAYLOAD),
            self._morph.morph(target),
        ]


class ChannelSelect:
    """SelectPort → ui.select.<region> + morph."""

    def __init__(self, morph: MorphPort | None = None) -> None:
        self._morph = morph or SMorph()

    def select(
        self,
        region: str,
        value: str,
        *,
        target: str | None = None,
    ) -> list[Op]:
        if not region or not isinstance(region, str):
            raise ValueError("select region must be a non-empty str")
        if not isinstance(value, str):
            raise ValueError("select value must be str")
        safe = region.replace(":", ".").replace("/", ".")
        key = f"{SELECT_PREFIX}{safe}"
        morph_target = target or region
        return [
            Op.kv_set(key, value),
            self._morph.morph(morph_target),
        ]


class ChannelConfirm:
    """ConfirmPort → composes OverlayPort with kind='confirm'."""

    def __init__(self, overlay: OverlayPort | None = None) -> None:
        self._overlay = overlay or ChannelOverlay()

    def ask(
        self,
        title: str,
        body: str,
        *,
        confirm_action: str,
        confirm_label: str = "Confirm",
        cancel_label: str = "Cancel",
        target: str = "overlay",
        **payload: Any,
    ) -> list[Op]:
        return self._overlay.open(
            "confirm",
            key="confirm",
            target=target,
            title=title,
            body=body,
            confirm_action=confirm_action,
            confirm_label=confirm_label,
            cancel_label=cancel_label,
            **payload,
        )


class TableTokens:
    """TokenPort backed by the elevated tokens tables.

    Import is lazy so this module does not hard-depend on ux-dom at
    import time when only overlay ports are needed.
    """

    def surface(self, level: str) -> str:
        from ux_dom.ui.tokens import surface as table

        return table[level]

    def target(self, size: str) -> str:
        from ux_dom.ui.tokens import target as table

        return table[size]

    def type_scale(self, step: str) -> str:
        from ux_dom.ui.tokens import type_scale as table

        return table[step]

    def ink(self, role: str) -> str:
        from ux_dom.ui.tokens import ink as table

        return table[role]


# ── Default bindings (Host can replace for tests / special surfaces) ────────
default_morph: MorphPort = SMorph()
default_overlay: OverlayPort = ChannelOverlay(default_morph)
default_select: SelectPort = ChannelSelect(default_morph)
default_confirm: ConfirmPort = ChannelConfirm(default_overlay)
default_tokens: TokenPort = TableTokens()


def form_result(
    *,
    ok: bool,
    message: str = "",
    target: str = "form",
    notices_target: str = "notices",
) -> list:
    """Design-level form outcome: morph form region + optional notice."""
    import html as _html

    from ux_app.ops import Op

    ops = [Op.ui_morph(target)]
    if message:
        safe = _html.escape(str(message))
        level = "success" if ok else "error"
        ops.append(Op.log_append(message, level=level))
        ops.append(Op.ui_morph(notices_target, {"text": safe, "level": level}))
    return ops
