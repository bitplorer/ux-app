"""Component field routing to Channel state after attach.

No ux_channel imports here — App._state is set by the adapter.
"""
from __future__ import annotations

from typing import Any

from ux_app.errors import ValidationError
from ux_app.state import FieldSpec

_LIVE_SESSION_PLANES = frozenset({"session", "sealed"})
_LIVE_CLIENT_PLANES = frozenset({"client"})
_DIRTY_PLANES = frozenset({"session", "store", "sealed"})


def _is_type(annotation: Any, expected: type) -> bool:
    return annotation is expected or annotation == expected.__name__


def field_key(component: Any, name: str, spec: FieldSpec | None = None) -> str:
    """Stable cell key for a component field.

    session / store / sealed / transient → ``{component.id}.{name}``
    client → allowlist key (or field name)
    """
    if spec is None:
        fields = getattr(type(component), "__ux_fields__", {}) or {}
        spec = fields.get(name)
    if spec is not None and spec.plane == "client":
        return str(spec.allowlist_key or name)
    ident = getattr(component, "id", None) or type(component).__name__.lower()
    return f"{ident}.{name}"


def live_state(inst: Any) -> Any:
    app = object.__getattribute__(inst, "_app")
    if app is None:
        return None
    return getattr(app, "_state", None)


def world_kv(app: Any) -> dict[str, Any] | None:
    peer = getattr(getattr(app, "runtime", None), "peer", None)
    if peer is None:
        return None
    world = getattr(peer, "world", None)
    if world is None:
        return None
    kv = getattr(world, "kv", None)
    return kv if isinstance(kv, dict) else None


def read_field(inst: Any, name: str, spec: FieldSpec) -> Any:
    values: dict[str, Any] = object.__getattribute__(inst, "_values")
    default = values.get(name, spec.default)
    st = live_state(inst)
    if st is not None and spec.plane in _LIVE_SESSION_PLANES:
        key = field_key(inst, name, spec)
        return st.session(key, default).get()
    if spec.plane == "store":
        app = object.__getattribute__(inst, "_app")
        if app is not None:
            key = field_key(inst, name, spec)
            kv = world_kv(app)
            if kv is not None and key in kv:
                return kv[key]
    return default


def write_field(inst: Any, name: str, spec: FieldSpec, value: Any) -> None:
    if spec.plane == "sealed" and _is_type(spec.annotation, int) and type(value) is not int:
        raise ValidationError(
            f"sealed field {name!r} must be int, got {type(value).__name__} (no coerce)",
            fields={name: "no coerce"},
        )
    values: dict[str, Any] = object.__getattribute__(inst, "_values")
    values[name] = value
    if spec.plane in _DIRTY_PLANES:
        object.__setattr__(inst, "_dirty", True)

    st = live_state(inst)
    app = object.__getattribute__(inst, "_app")
    if st is not None and spec.plane in _LIVE_SESSION_PLANES:
        key = field_key(inst, name, spec)
        st.session(key, values.get(name, spec.default)).set(value)
        return
    if st is not None and spec.plane in _LIVE_CLIENT_PLANES:
        path = field_key(inst, name, spec)
        allow = set(getattr(getattr(app, "runtime", None), "client_state", ()) or ())
        persist = path in allow
        st.client.set(path, value, persist=persist)
        return
    if spec.plane == "store" and app is not None:
        key = field_key(inst, name, spec)
        kv = world_kv(app)
        if kv is not None:
            kv[key] = value
