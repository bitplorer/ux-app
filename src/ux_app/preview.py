"""Peer-local preview. Not an Op. Never lineage. No Channel imports."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class PreviewCall:
    """Marker returned by preview helpers. Illegal inside Action Ops."""

    kind: str
    payload: dict[str, Any]


@dataclass
class Preview:
    pending_targets: dict[str, bool] = field(default_factory=dict)
    shadows: dict[str, Any] = field(default_factory=dict)
    filters: dict[str, Any] = field(default_factory=dict)

    def pending(self, target: str, busy: bool = True) -> PreviewCall:
        self.pending_targets[target] = bool(busy)
        return PreviewCall("pending", {"target": target, "busy": busy})

    def update(self, target: str, patch: Any) -> PreviewCall:
        self.shadows[target] = patch
        return PreviewCall("update", {"target": target, "patch": patch})

    def filter(self, kv_key: str, q: Any, out: str) -> PreviewCall:
        self.filters[out] = {"key": kv_key, "q": q}
        return PreviewCall("filter", {"key": kv_key, "q": q, "out": out})

    def clear(self) -> None:
        self.pending_targets.clear()
        self.shadows.clear()
        self.filters.clear()

    def is_empty(self) -> bool:
        return not self.pending_targets and not self.shadows and not self.filters


preview = Preview()
