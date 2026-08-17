"""Drop-in Component. A class with id + render is enough."""

from __future__ import annotations

from typing import Any, Callable

from ux_app.field_planes import field_key, read_field, write_field
from ux_app.state import FieldSpec, collect_fields


class Component:
    """UI unit with a stable id and render().

    Dataclass-style annotated fields default to the session plane.
    After ``App.attach``, session/sealed fields read and write Channel
    draft; client fields emit Channel client ops. store/transient stay
    local (store may mirror ``world.kv``). Get always returns a plain
    value — never a Channel handle.
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
            "field_key",
        }:
            return object.__getattribute__(self, name)
        fields = object.__getattribute__(type(self), "__dict__").get("__ux_fields__")
        if fields and name in fields:
            return read_field(self, name, fields[name])
        return object.__getattribute__(self, name)

    def __setattr__(self, name: str, value: Any) -> None:
        fields: dict[str, FieldSpec] = getattr(type(self), "__ux_fields__", {})
        if name in fields:
            write_field(self, name, fields[name], value)
            return
        object.__setattr__(self, name, value)

    @property
    def field_specs(self) -> dict[str, FieldSpec]:
        return getattr(type(self), "__ux_fields__", {})

    def field_key(self, name: str) -> str:
        specs = getattr(type(self), "__ux_fields__", {}) or {}
        return field_key(self, name, specs.get(name))

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
