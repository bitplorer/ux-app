"""Drop-in Component. A class with id + render is enough."""

from __future__ import annotations

from typing import Any, Callable

from ux_app.errors import ValidationError
from ux_app.state import FieldSpec, collect_fields


def _is_type(annotation: Any, expected: type) -> bool:
    return annotation is expected or annotation == expected.__name__


def field_key(component_id: str, name: str, spec: FieldSpec) -> str:
    """Stable key for live session cells: ``{id}.{field}``.

    Client plane uses ``spec.allowlist_key`` (or the field name) as the
    browser path — not this helper.
    """
    ident = (component_id or "").strip() or "component"
    return f"{ident}.{name}"


def _live_state(app: Any) -> Any:
    if app is None:
        return None
    return getattr(app, "_state", None)


def _read_field(inst: Any, name: str, spec: FieldSpec) -> Any:
    values: dict[str, Any] = object.__getattribute__(inst, "_values")
    default = values.get(name, spec.default)
    app = object.__getattribute__(inst, "_app")
    st = _live_state(app)

    if st is not None and spec.plane == "session":
        key = field_key(getattr(inst, "id", "") or "", name, spec)
        cell = st.session(key, default)
        return cell.get()

    # client / store / transient / sealed: instance mirror (client also
    # mirrors so SSR first paint stays coherent).
    return default


def _write_field(inst: Any, name: str, spec: FieldSpec, value: Any) -> None:
    values: dict[str, Any] = object.__getattribute__(inst, "_values")
    app = object.__getattribute__(inst, "_app")
    st = _live_state(app)

    if spec.plane == "session":
        if st is not None:
            key = field_key(getattr(inst, "id", "") or "", name, spec)
            st.session(key, spec.default).set(value)
        values[name] = value
        object.__setattr__(inst, "_dirty", True)
        return

    if spec.plane == "client":
        values[name] = value
        if st is not None:
            path = spec.allowlist_key or name
            # Pending browser ops; server mirror is values[name].
            st.client.set(path, value)
        return

    if spec.plane == "store":
        values[name] = value
        object.__setattr__(inst, "_dirty", True)
        # Optional world.kv mirror when bound — durable across peer apply.
        if app is not None:
            runtime = getattr(app, "runtime", None)
            peer = getattr(runtime, "peer", None)
            world = getattr(peer, "world", None)
            if world is not None and hasattr(world, "kv"):
                world.kv[field_key(getattr(inst, "id", "") or "", name, spec)] = value
        return

    if spec.plane == "sealed":
        values[name] = value
        object.__setattr__(inst, "_dirty", True)
        return

    # transient
    values[name] = value


class Component:
    """UI unit with a stable id and render().

    Dataclass-style annotated fields default to the session plane.
    After ``App.attach``, session fields read/write Channel draft via
    ``{id}.{field}`` keys; client fields enqueue browser ops through
    Channel's client plane (allowlisted). Offline / tests keep using
    the in-process ``_values`` bag.
    """

    id: str = ""

    def __init_subclass__(cls, **kwargs: Any) -> None:
        super().__init_subclass__(**kwargs)
        cls.__ux_fields__ = collect_fields(cls)

    def __init__(self, **kwargs: Any) -> None:
        object.__setattr__(self, "_values", {})
        object.__setattr__(self, "_dirty", False)
        object.__setattr__(self, "_app", None)
        fields: dict[str, FieldSpec] = getattr(type(self), "__ux_fields__", {})
        for name, spec in fields.items():
            if name in kwargs:
                # Must go through __setattr__ so sealed ints refuse coerce.
                setattr(self, name, kwargs[name])
            else:
                self._values[name] = spec.default

    def __getattribute__(self, name: str) -> Any:
        if name.startswith("_") or name in {
            "id",
            "render",
            "to_html",
            "is_dirty",
            "clear_dirty",
            "bind_app",
            "field_specs",
        }:
            return object.__getattribute__(self, name)
        fields = object.__getattribute__(type(self), "__dict__").get("__ux_fields__")
        if fields and name in fields:
            return _read_field(self, name, fields[name])
        return object.__getattribute__(self, name)

    def __setattr__(self, name: str, value: Any) -> None:
        fields: dict[str, FieldSpec] = getattr(type(self), "__ux_fields__", {})
        if name in fields:
            spec = fields[name]
            if spec.plane == "sealed" and _is_type(spec.annotation, int) and type(value) is not int:
                raise ValidationError(
                    f"sealed field {name!r} must be int, got {type(value).__name__} (no coerce)",
                    fields={name: "no coerce"},
                )
            _write_field(self, name, spec, value)
            return
        object.__setattr__(self, name, value)

    @property
    def field_specs(self) -> dict[str, FieldSpec]:
        return getattr(type(self), "__ux_fields__", {})

    def is_dirty(self) -> bool:
        return bool(getattr(self, "_dirty", False))

    def clear_dirty(self) -> None:
        object.__setattr__(self, "_dirty", False)

    def bind_app(self, app: Any) -> None:
        object.__setattr__(self, "_app", app)

    def render(self) -> Any:
        raise NotImplementedError(f"{type(self).__name__}.render() is required")

    def to_html(self, *, mint: Callable[[Any], dict[str, str]] | None = None) -> str:
        from ux_app.html import Element, _child_html

        tree = self.render()
        if isinstance(tree, str):
            return tree
        if isinstance(tree, Element):
            return tree.to_html(mint=mint)
        return _child_html(tree, mint=mint)


def is_component(obj: Any) -> bool:
    ident = getattr(obj, "id", None)
    render = getattr(obj, "render", None)
    return bool(ident) and callable(render)
