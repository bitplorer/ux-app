# Copyright (c) 2026 ux-app
"""Stable ports for the channel-native design system.

Product Actions and composites depend on these protocols.
Concrete kv keys, morph target defaults, and session shape live in
adapters (see adapters.py). If storage or morph strategy changes,
fix the adapter — not the surface.
"""

from __future__ import annotations

from typing import Any, Protocol, runtime_checkable

from ux_app.ops import Op

__all__ = [
    "OverlayPort",
    "SelectPort",
    "MorphPort",
    "TokenPort",
    "ConfirmPort",
]


@runtime_checkable
class MorphPort(Protocol):
    """Produce a single morph Op for a stamped region / Component id."""

    def morph(self, target: str, patch: Any = None) -> Op: ...


@runtime_checkable
class OverlayPort(Protocol):
    """Open / close the Channel-driven overlay cell."""

    def open(
        self,
        kind: str,
        *,
        key: str | None = None,
        target: str = "overlay",
        **payload: Any,
    ) -> list[Op]: ...

    def close(self, *, target: str = "overlay") -> list[Op]: ...


@runtime_checkable
class SelectPort(Protocol):
    """Select a tab / carousel page / accordion item."""

    def select(
        self,
        region: str,
        value: str,
        *,
        target: str | None = None,
    ) -> list[Op]: ...


@runtime_checkable
class ConfirmPort(Protocol):
    """Design-level confirm dialog (usually composes OverlayPort)."""

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
    ) -> list[Op]: ...


@runtime_checkable
class TokenPort(Protocol):
    """Resolve design tokens to class strings."""

    def surface(self, level: str) -> str: ...
    def target(self, size: str) -> str: ...
    def type_scale(self, step: str) -> str: ...
    def ink(self, role: str) -> str: ...
