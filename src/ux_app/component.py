"""Drop-in Component. A class with id + render is enough."""

from __future__ import annotations

from typing import Any, Callable

from ux_app.errors import ValidationError
from ux_app.state import FieldSpec, collect_fields


def _is_type(annotation: Any, expected: type) -> bool:
    return annotation is expected or annotation == expected.__name__



class Component:
    """UI unit with a stable id and render().

    Dataclass-style annotated fields default to the session plane.
    Honor ux-dom Component / ReactiveComponent if the author subclasses
    those instead — this class is optional.
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
            return object.__getattribute__(self, "_values").get(name, fields[name].default)
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
            self._values[name] = value
            if spec.plane in {"session", "store", "sealed"}:
                object.__setattr__(self, "_dirty", True)
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
