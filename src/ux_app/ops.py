"""Ops and author macros.

Helpers expand to legal pairs. They are not a second protocol.
Construction validates pair *structure*. The session stamp is enforced
at emit (submit / apply), so authors can write ``Op("search", "hits", …)``
after ``app.use("search")`` without threading the stamp by hand.
"""

from __future__ import annotations

import html
from typing import Any, Iterable, Mapping, Sequence

from ux_app.errors import IllegalOp

S_PAIRS: frozenset[tuple[str, str]] = frozenset(
    {
        ("kv", "set"),
        ("kv", "delete"),
        ("log", "append"),
        ("ui.dom", "morph"),
        ("ui.dom", "restore"),
    }
)

FORBIDDEN_NS_PREFIXES = ("cek.", "sys.", "_")
RESERVED_BASELINE = frozenset({"kv", "log"})
MAX_NS_DOTS = 2


def name_is_token(name: str) -> bool:
    return bool(name) and all(c.islower() or c.isdigit() for c in name)


def fq_of(ns: str, name: str) -> str:
    return f"{ns}.{name}"


def validate_pair(ns: str, name: str, *, allow_reserved: bool | None = None) -> None:
    if not ns:
        raise IllegalOp("domain name is empty")
    if ns.startswith(".") or ns.endswith("."):
        raise IllegalOp(f"domain '{ns}' has leading/trailing dot")
    if ".." in ns:
        raise IllegalOp(f"domain '{ns}' contains empty segment")
    if ns.count(".") > MAX_NS_DOTS:
        raise IllegalOp(f"domain '{ns}' has too many dots (max {MAX_NS_DOTS})")
    for prefix in FORBIDDEN_NS_PREFIXES:
        if ns.startswith(prefix):
            raise IllegalOp(f"domain '{ns}' uses forbidden prefix '{prefix}'")
    allow = ns in {"kv", "log", "ui.dom"} if allow_reserved is None else allow_reserved
    if not allow and ns in RESERVED_BASELINE:
        raise IllegalOp(f"domain '{ns}' is reserved Baseline")
    if not all(c.islower() or c.isdigit() or c == "." for c in ns):
        raise IllegalOp(f"domain '{ns}' has invalid characters")
    if not name:
        raise IllegalOp("op name is empty")
    if "." in name:
        raise IllegalOp(f"op name '{name}' must not contain dots (dots belong in ns)")
    if not name_is_token(name):
        raise IllegalOp(f"op name '{name}' has invalid characters")


def is_s_pair(ns: str, name: str) -> bool:
    return (ns, name) in S_PAIRS


class Op:
    """One ordered effect. Identity is the pair (ns, name)."""

    __slots__ = ("ns", "name", "payload")

    def __init__(
        self,
        ns: str,
        name: str,
        payload: dict[str, Any] | None = None,
        *,
        stamp: frozenset[tuple[str, str]] | None = None,
    ) -> None:
        validate_pair(ns, name)
        pair = (ns, name)
        if stamp is not None and pair not in stamp:
            raise IllegalOp(f"illegal pair: {fq_of(ns, name)} — absent from session stamp")
        self.ns = ns
        self.name = name
        self.payload = dict(payload or {})

    @staticmethod
    def stamped(
        ns: str,
        name: str,
        payload: dict[str, Any] | None,
        stamp: frozenset[tuple[str, str]],
    ) -> "Op":
        return Op(ns, name, payload, stamp=stamp)

    def to_dict(self) -> dict[str, Any]:
        return {"ns": self.ns, "name": self.name, "payload": dict(self.payload)}

    @property
    def pair(self) -> tuple[str, str]:
        return (self.ns, self.name)

    @property
    def fq(self) -> str:
        return fq_of(self.ns, self.name)

    def __repr__(self) -> str:
        return f"Op({self.fq}, {self.payload!r})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Op):
            return NotImplemented
        return self.ns == other.ns and self.name == other.name and self.payload == other.payload

    @staticmethod
    def kv_set(key: str, value: Any) -> "Op":
        _nonempty(key, "kv.set key")
        return Op("kv", "set", {"key": key, "value": value})

    @staticmethod
    def kv_delete(key: str, prior: Any | None = None) -> "Op":
        _nonempty(key, "kv.delete key")
        p: dict[str, Any] = {"key": key}
        if prior is not None:
            p["prior"] = prior
        return Op("kv", "delete", p)

    @staticmethod
    def ui_morph(target: str, patch: Any = None, snapshot: Any | None = None) -> "Op":
        _nonempty(target, "ui.dom.morph target")
        p: dict[str, Any] = {"target": target, "patch": patch}
        if snapshot is not None:
            p["snapshot"] = snapshot
        return Op("ui.dom", "morph", p)

    @staticmethod
    def ui_restore(target: str, snapshot: Any) -> "Op":
        _nonempty(target, "ui.dom.restore target")
        return Op("ui.dom", "restore", {"target": target, "snapshot": snapshot})

    @staticmethod
    def log_append(
        message: str, *, level: str = "info", fields: Mapping[str, Any] | None = None
    ) -> "Op":
        if not isinstance(message, str):
            raise IllegalOp("log.append message must be str")
        p: dict[str, Any] = {"message": html.escape(message), "level": level}
        if fields:
            p["fields"] = dict(fields)
        return Op("log", "append", p)


def _nonempty(v: Any, label: str) -> None:
    if not isinstance(v, str) or not v.strip():
        raise IllegalOp(f"{label} must be non-empty str")


def update(target: str, patch: Any = None) -> Op:
    """Re-render that Component. Macro → ui.dom.morph."""
    return Op.ui_morph(target, patch)


def notify(text: str, *, level: str = "info") -> list[Op]:
    """Transient user message. Lowers to log.append + morph of notices.

    Never emits undeclared ui.toast. A rich notice pack is a domain.
    """
    safe = html.escape(str(text))
    return [
        Op.log_append(text, level=level),
        Op.ui_morph("notices", {"text": safe, "level": level}),
    ]


def go(path: str, *, title: str | None = None) -> list[Op]:
    """Change location. Lowers to kv.set(ui:nav) + optional morph.

    Never emits undeclared nav.push.
    """
    _nonempty(path, "go path")
    loc = {"path": path, "title": title}
    return [
        Op.kv_set("ui:nav", loc),
        Op.ui_morph("content", {"path": path, "title": title}),
    ]


def store_set(key: str, value: Any) -> Op:
    """Session/store write. Macro → kv.set."""
    return Op.kv_set(key, value)


def as_ops(value: Any) -> list[Op]:
    """Normalize an Action return to list[Op]. Rejects preview calls."""
    from ux_app.preview import PreviewCall

    if value is None:
        return []
    if isinstance(value, PreviewCall):
        raise IllegalOp("preview is not an Op; do not return it from an Action")
    if isinstance(value, Op):
        return [value]
    if isinstance(value, (list, tuple)):
        out: list[Op] = []
        for item in value:
            if isinstance(item, PreviewCall):
                raise IllegalOp("preview is not an Op; do not return it from an Action")
            if isinstance(item, Op):
                out.append(item)
            elif isinstance(item, (list, tuple)):
                out.extend(as_ops(item))
            else:
                raise IllegalOp(f"Action must return list[Op], got {type(item).__name__}")
        return out
    raise IllegalOp(f"Action must return list[Op], got {type(value).__name__}")


def check_stamp(ops: Sequence[Op], stamp: Iterable[tuple[str, str]]) -> None:
    allowed = frozenset(stamp)
    for op in ops:
        if op.pair not in allowed:
            raise IllegalOp(f"illegal pair: {op.fq} — absent from session stamp")
