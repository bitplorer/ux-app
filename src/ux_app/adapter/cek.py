"""Thin wrap of Channel's CEK door. Empty when cek=off.

Application code never imports this. Only adapter/boot.py calls attach().
"""

from __future__ import annotations

from typing import Any


def attach(channel: Any, *, mode: str) -> str | None:
    """Reach CEK only through ux_channel.cek. Never import cek_surface here.

    ``off``    — no CEK import.
    ``adapt``  — optional; missing extra is a note, not a crash.
    ``require``— missing extra is an error for the caller to surface.
    """
    if mode == "off" or channel is None:
        return None
    try:
        import ux_channel  # noqa: F401
    except ImportError:
        if mode == "require":
            raise RuntimeError("cek=require needs ux-channel") from None
        return "cek extra requested but ux-channel is not installed"
    cek_mod = getattr(ux_channel, "cek", None)
    if cek_mod is None:
        if mode == "require":
            raise RuntimeError("ux_channel.cek is missing (install ux-channel[cek])")
        return "ux_channel.cek is not available"
    # Presence is enough. We do not re-export chrome / arm / Surface.
    return f"cek door attached mode={mode}"
