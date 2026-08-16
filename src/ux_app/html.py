"""Tiny element tree so on_click= can mint Caps. No Channel imports."""

from __future__ import annotations

import html
from typing import Any, Callable, Iterable


class Element:
    __slots__ = ("tag", "children", "attrs")

    def __init__(self, tag: str, children: Iterable[Any] = (), **attrs: Any) -> None:
        self.tag = tag
        self.children = list(children)
        self.attrs = dict(attrs)

    def to_html(self, *, mint: Callable[[Any], dict[str, str]] | None = None) -> str:
        attrs: dict[str, str] = {}
        for key, value in self.attrs.items():
            if key in {"on_click", "on_submit"} and callable(value):
                extra = mint(value) if mint is not None else {}
                for ek, ev in extra.items():
                    attrs[ek] = html.escape(str(ev), quote=True)
                continue
            if value is None or value is False:
                continue
            if value is True:
                attrs[key.replace("_", "-")] = key.replace("_", "-")
                continue
            attrs[key.replace("_", "-")] = html.escape(str(value), quote=True)
        inner = "".join(_child_html(c, mint=mint) for c in self.children)
        if not attrs:
            return f"<{self.tag}>{inner}</{self.tag}>"
        attr_s = "".join(f' {k}="{v}"' for k, v in attrs.items())
        return f"<{self.tag}{attr_s}>{inner}</{self.tag}>"


def _child_html(child: Any, *, mint: Callable[[Any], dict[str, str]] | None) -> str:
    if child is None:
        return ""
    if isinstance(child, Element):
        return child.to_html(mint=mint)
    if isinstance(child, (list, tuple)):
        return "".join(_child_html(c, mint=mint) for c in child)
    return html.escape(str(child))


def el(tag: str, *children: Any, **attrs: Any) -> Element:
    return Element(tag, children, **attrs)


def Badge(count: Any, *, on_click: Any = None, **attrs: Any) -> Element:
    """Day-1 control. Renders a button whose label is the count."""
    if on_click is not None:
        attrs["on_click"] = on_click
    attrs.setdefault("type", "button")
    attrs.setdefault("class", "rounded bg-slate-900 px-3 py-1 text-white")
    return el("button", str(count), **attrs)
