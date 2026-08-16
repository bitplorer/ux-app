"""Host answer. Author code should not construct this by hand."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from ux_app.ops import Op


@dataclass
class Result:
    ok: bool
    ops: list[Op] = field(default_factory=list)
    kind: str = "ok"
    error: str | None = None
    meta: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "ok": self.ok,
            "ops": [o.to_dict() for o in self.ops],
            "kind": self.kind,
            "error": self.error,
            "meta": dict(self.meta),
        }


def ok(ops: list[Op] | None = None, **meta: Any) -> Result:
    return Result(ok=True, ops=list(ops or []), kind="ok", meta=meta)


def authority_refusal(reason: str) -> Result:
    return Result(ok=False, ops=[], kind="authority_refusal", error=reason)


def dispatch_error(reason: str) -> Result:
    return Result(ok=False, ops=[], kind="dispatch_error", error=reason)
