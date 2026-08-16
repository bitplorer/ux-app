"""Stand up Document + Channel when the cores are installed.

Lazy-imports only. A missing core is not a crash — App.boot() falls
back to the in-process LocalRuntime so day-1 and tests work without
unpublished GitHub packages.

Attach order is law: Peer kernel **then** preview (C-pre-05).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

KERNEL_SCRIPT = "ux-peer-kernel.js"
PREVIEW_SCRIPT = "ux-peer-perception.js"

# Kernel first, preview second. Never reverse.
SCRIPT_ORDER: tuple[tuple[str, str], ...] = (
    (KERNEL_SCRIPT, "peer-kernel"),
    (PREVIEW_SCRIPT, "preview"),
)


@dataclass
class BootResult:
    title: str
    cek: str
    document: Any = None
    channel: Any = None
    cores_present: bool = False
    scripts: tuple[tuple[str, str], ...] = SCRIPT_ORDER
    notes: list[str] = field(default_factory=list)


def try_boot(
    title: str = "App",
    *,
    cek: str = "off",
    profile: str = "ui",
) -> BootResult:
    """Attempt to attach live cores. Never imports them at module level."""
    result = BootResult(title=title, cek=cek)
    document = _try_document(title)
    channel = _try_channel(cek=cek, profile=profile)
    result.document = document
    result.channel = channel
    result.cores_present = document is not None and channel is not None
    if document is None:
        result.notes.append("ux-dom not installed; using in-process document")
    if channel is None:
        result.notes.append("ux-channel not installed; using in-process Host+Peer")
    if cek != "off":
        from ux_app.adapter.cek import attach as attach_cek

        note = attach_cek(channel, mode=cek)
        if note:
            result.notes.append(note)
    return result


def _try_document(title: str) -> Any:
    try:
        from ux_app.adapter import document as document_mod
    except Exception:
        return None
    return document_mod.try_document(title)


def _try_channel(*, cek: str, profile: str) -> Any:
    try:
        from ux_app.adapter import channel as channel_mod
    except Exception:
        return None
    return channel_mod.try_channel(cek=cek, profile=profile)
