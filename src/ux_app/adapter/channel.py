"""Lazy Channel bind. The only place ux_channel may be imported."""

from __future__ import annotations

from typing import Any


def try_channel(*, cek: str = "off", profile: str = "ui") -> Any:
    """Return a live Channel if ux_channel is importable, else None.

    Does not invent a second wire. When the package is missing the
    in-process LocalRuntime is the Host+Peer for tests and day-1.
    """
    try:
        import ux_channel  # noqa: F401
    except ImportError:
        return None
    # Live API may move. Detect presence; do not guess constructors.
    return {
        "module": "ux_channel",
        "cek": cek,
        "profile": profile,
        "impl": ux_channel,
    }


def present() -> bool:
    try:
        import ux_channel  # noqa: F401

        return True
    except ImportError:
        return False
