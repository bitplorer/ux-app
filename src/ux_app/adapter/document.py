"""Lazy Document bind. The only place ux_dom may be imported."""

from __future__ import annotations

from typing import Any


def try_document(title: str) -> Any:
    """Return a live Document if ux_dom is importable, else None."""
    try:
        import ux_dom  # noqa: F401
    except ImportError:
        return None
    return {
        "module": "ux_dom",
        "title": title,
        "impl": ux_dom,
    }


def present() -> bool:
    try:
        import ux_dom  # noqa: F401

        return True
    except ImportError:
        return False
