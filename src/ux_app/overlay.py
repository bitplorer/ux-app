# Copyright (c) 2026 ux-app
"""Channel-first overlay macros — author façade.

Authors call open_overlay / close_overlay / select_region / confirm.
These delegate to OverlayPort / SelectPort / ConfirmPort defaults.

Concrete kv keys and morph strategy live in adapters.py.
If the session scheme or morph driver changes, fix the adapter —
product Actions and this façade stay stable.

Elevation rule: if batching Ops is a recurring design-system pattern,
add a method on a port + a macro here. Do not leave design-level
batches in product Actions.
"""

from __future__ import annotations

from typing import Any

from ux_app.adapters import (
    default_confirm,
    default_overlay,
    default_select,
    form_result as _form_result,
)
from ux_app.ops import Op
from ux_app.ports import ConfirmPort, OverlayPort, SelectPort

__all__ = [
    "open_overlay",
    "close_overlay",
    "select_region",
    "confirm",
    "form_result",
    "bind_overlay",
    "bind_select",
    "bind_confirm",
]

# Mutable defaults so tests / special Hosts can inject alternate ports
_overlay: OverlayPort = default_overlay
_select: SelectPort = default_select
_confirm: ConfirmPort = default_confirm


def bind_overlay(port: OverlayPort) -> None:
    """Replace the OverlayPort used by open_overlay / close_overlay."""
    global _overlay
    _overlay = port


def bind_select(port: SelectPort) -> None:
    """Replace the SelectPort used by select_region."""
    global _select
    _select = port


def bind_confirm(port: ConfirmPort) -> None:
    """Replace the ConfirmPort used by confirm."""
    global _confirm
    _confirm = port


def open_overlay(
    kind: str,
    *,
    key: str | None = None,
    target: str = "overlay",
    **payload: Any,
) -> list[Op]:
    """Open a Channel-driven overlay (dialog / sheet / command / popover).

    ::

        @action("lot.show", caps=())
        def show_lot(ctx, lot_id: str):
            return open_overlay("dialog", key="lot", lot_id=lot_id)
    """
    return _overlay.open(kind, key=key, target=target, **payload)


def close_overlay(*, target: str = "overlay") -> list[Op]:
    """Close the Channel-driven overlay cell.

    ::

        @action("ui.close", caps=())
        def close(ctx):
            return close_overlay()
    """
    return _overlay.close(target=target)


def select_region(
    region: str,
    value: str,
    *,
    target: str | None = None,
) -> list[Op]:
    """Select a tab / carousel page / accordion item via Channel.

    ::

        @action("nav.tab", caps=())
        def switch(ctx, tab: str):
            return select_region("tabs:main", tab)
    """
    return _select.select(region, value, target=target)


def confirm(
    title: str,
    body: str,
    *,
    confirm_action: str,
    confirm_label: str = "Confirm",
    cancel_label: str = "Cancel",
    target: str = "overlay",
    **payload: Any,
) -> list[Op]:
    """Open a confirm dialog — design-level batch behind one interface.

    ::

        @action("order.delete.ask", caps=())
        def ask_delete(ctx, order_id: str):
            return confirm(
                "Delete order?",
                "This cannot be undone.",
                confirm_action="order.delete",
                order_id=order_id,
            )
    """
    return _confirm.ask(
        title,
        body,
        confirm_action=confirm_action,
        confirm_label=confirm_label,
        cancel_label=cancel_label,
        target=target,
        **payload,
    )


def form_result(
    *,
    ok: bool,
    message: str = "",
    target: str = "form",
    notices_target: str = "notices",
) -> list[Op]:
    """Morph form region + optional notice — design-level batch."""
    return _form_result(
        ok=ok, message=message, target=target, notices_target=notices_target
    )
