"""Follow-up Actions. Host-issued continuation Caps. No Channel types."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class Continuation:
    event: str
    action: str
    cap: str
    args_from: dict[str, str] = field(default_factory=dict)
    args: dict[str, Any] = field(default_factory=dict)


_CURRENT: list[Continuation] | None = None


def _begin_follow_ups() -> list[Continuation]:
    global _CURRENT
    bucket: list[Continuation] = []
    _CURRENT = bucket
    return bucket


def _end_follow_ups() -> list[Continuation]:
    global _CURRENT
    out = list(_CURRENT or [])
    _CURRENT = None
    return out


def follow_up(
    event: str,
    action: str,
    args_from: dict[str, str] | None = None,
    **args: Any,
) -> Continuation:
    """Record a Host-issued next step. Prefer ctx.follow_up during an Action."""
    item = Continuation(
        event=event,
        action=action,
        cap="",
        args_from=dict(args_from or {}),
        args=dict(args),
    )
    if _CURRENT is not None:
        _CURRENT.append(item)
    return item
