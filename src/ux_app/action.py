"""Named Actions. Return list[Op]. No Channel types."""

from __future__ import annotations

import inspect
from dataclasses import dataclass, field
from typing import Any, Callable

from ux_app.errors import ValidationError


@dataclass
class ActionSpec:
    name: str
    fn: Callable[..., Any]
    caps: tuple[str, ...]
    component_id: str | None = None
    method: str | None = None
    public: bool = False
    is_async: bool = False
    params: dict[str, inspect.Parameter] = field(default_factory=dict)


_REGISTRY: dict[str, ActionSpec] = {}


def action(name: str, *, caps: list[str] | tuple[str, ...] | None = None) -> Callable:
    """Register a named server function.

    ``caps=`` is required. Pass ``caps=()`` for the explicit public opt-out.
    """

    if caps is None:
        raise TypeError(
            f"@action({name!r}) requires caps=[...] "
            "(use caps=() for the explicit public opt-out)"
        )

    def deco(fn: Callable[..., Any]) -> Callable[..., Any]:
        spec = ActionSpec(
            name=name,
            fn=fn,
            caps=tuple(caps),
            public=len(tuple(caps)) == 0,
            is_async=inspect.iscoroutinefunction(fn),
            params=dict(inspect.signature(fn).parameters),
        )
        _REGISTRY[name] = spec
        fn.__ux_action__ = spec  # type: ignore[attr-defined]
        return fn

    return deco


def get_action(name: str) -> ActionSpec | None:
    return _REGISTRY.get(name)


def all_actions() -> dict[str, ActionSpec]:
    return dict(_REGISTRY)


def clear_actions() -> None:
    _REGISTRY.clear()


def validate_args(spec: ActionSpec, args: dict[str, Any]) -> dict[str, Any]:
    """Fail before the body. Integer params: no silent coerce."""
    out = dict(args)
    for pname, param in spec.params.items():
        if pname in {"ctx", "self", "cls"}:
            continue
        if pname not in out:
            if param.default is not inspect.Parameter.empty:
                continue
            raise ValidationError(
                f"missing argument {pname!r}",
                fields={pname: "required"},
            )
        value = out[pname]
        annotation = param.annotation
        if _is_type(annotation, int) and type(value) is not int:
            raise ValidationError(
                f"{pname!r} must be int, got {type(value).__name__} (no coerce)",
                fields={pname: "no coerce"},
            )
        if _is_type(annotation, str) and type(value) is not str:
            raise ValidationError(
                f"{pname!r} must be str, got {type(value).__name__}",
                fields={pname: "type"},
            )
    return out


def _is_type(annotation: Any, expected: type) -> bool:
    return annotation is expected or annotation == expected.__name__

