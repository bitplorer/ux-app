"""Dataclass-style field planes. No Channel / CEK imports."""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any

MONEY_SHAPED = re.compile(
    r"(price|amount|balance|qty|quantity|cost|total|secret|password|role|token|ssn|cvv)",
    re.I,
)

PLANES = ("session", "client", "store", "transient", "sealed")


@dataclass(frozen=True)
class FieldMarker:
    plane: str
    default: Any = None
    allowlist_key: str | None = None


def Client(default: Any = None, *, key: str | None = None) -> FieldMarker:
    return FieldMarker("client", default, key)


def Store(default: Any = None) -> FieldMarker:
    return FieldMarker("store", default)


def Transient(default: Any = None) -> FieldMarker:
    return FieldMarker("transient", default)


def Sealed(default: Any = None) -> FieldMarker:
    return FieldMarker("sealed", default)


def Session(default: Any = None) -> FieldMarker:
    return FieldMarker("session", default)


@dataclass(frozen=True)
class FieldSpec:
    name: str
    annotation: Any
    default: Any
    plane: str
    allowlist_key: str | None = None


def collect_fields(cls: type) -> dict[str, FieldSpec]:
    fields: dict[str, FieldSpec] = {}
    annotations = getattr(cls, "__annotations__", {}) or {}
    for name, annotation in annotations.items():
        if name in {"id"}:
            continue
        raw = getattr(cls, name, None)
        if isinstance(raw, FieldMarker):
            fields[name] = FieldSpec(
                name=name,
                annotation=annotation,
                default=raw.default,
                plane=raw.plane,
                allowlist_key=raw.allowlist_key or name,
            )
        else:
            fields[name] = FieldSpec(
                name=name,
                annotation=annotation,
                default=raw,
                plane="session",
            )
    return fields


def is_money_shaped(name: str) -> bool:
    return bool(MONEY_SHAPED.search(name))
