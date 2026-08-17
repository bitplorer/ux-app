"""Lazy Channel bind. The only place ux_channel may be imported.

Product apps never construct Channel or mint channel caps.
They call ``App.attach(asgi)``, ``App.region(render)``, ``App.control(...)``.
"""

from __future__ import annotations

import inspect
import json
import os
from typing import Any, Callable

from ux_app.errors import DispatchError

# Channel speech: one morphable DOM slot is a Region (NAMING.md).
# Default uid follows Channel's dotted app.* pattern (see app.flash).
DEFAULT_REGION_UID = "app.root"


def try_channel(*, cek: str = "off", profile: str = "ui") -> Any:
    """Return a presence handle if ux_channel is importable, else None.

    Does not invent a second wire. ``App.attach`` is what mounts the host.
    When the package is missing the in-process LocalRuntime is the Host+Peer.
    """
    try:
        import ux_channel  # noqa: F401
    except ImportError:
        return None
    return {
        "module": "ux_channel",
        "cek": cek,
        "profile": profile,
        "impl": ux_channel,
    }


def present() -> bool:
    try:
        import ux_channel  # noqa: F401

        return True
    except ImportError:
        return False


def attach(
    host: Any,
    asgi: Any,
    *,
    secret: str | None = None,
    path: str = "/ux-channel",
    region: Callable[[], Any] | None = None,
    uid: str | None = None,
) -> Any:
    """Boot the live Channel *behind* App. Returns the wire or None.

    Registers one Region that forwards Actions to ``host.submit``.
    Product modules must not call this — use ``App.attach``.
    """
    if region is not None:
        host._region_render = region
    if uid:
        host._region_uid = uid
    if getattr(host, "_wire", None) is not None:
        return host._wire
    if asgi is None:
        return None
    try:
        from ux_channel import Channel, ChannelConfig
    except ImportError:
        return None

    secret = (
        secret
        or os.environ.get("UX_CHANNEL_SECRET")
        or os.environ.get("UX_APP_SECRET")
        or "dev-secret-key-32chars-minimum!!!!"
    )
    if os.environ.get("REDIS_URL"):
        cfg = ChannelConfig.production(secret).with_redis(os.environ["REDIS_URL"])
    else:
        cfg = ChannelConfig.development(secret=secret, allow_memory_stores=True)

    ch = Channel.boot(asgi, config=cfg, path=path)

    # Session · client façade (Channel state). Product reads fields on
    # Components; this is the only place ux_channel.state is imported.
    try:
        from ux_channel import state as channel_state

        allow = tuple(
            getattr(getattr(host, "runtime", None), "client_state", ()) or ()
        )
        host._state = channel_state(ch, allow=allow)
    except Exception:
        # Channel without state module — leave host._state unset.
        host._state = getattr(host, "_state", None)

    slot_uid = getattr(host, "_region_uid", None) or DEFAULT_REGION_UID

    def _paint(ctx=None):
        fn = getattr(host, "_region_render", None)
        if not callable(fn):
            return ""
        tree = fn()
        if tree is None:
            return ""
        if hasattr(tree, "__render__"):
            return tree.__render__(pretty=False)
        return str(tree)

    # Channel owns region attach. Adapter only forwards the host render.
    slot = ch.region(slot_uid)(_paint)

    @ch.on("ux_app.dispatch", refresh=[slot], idempotent=False)
    def dispatch(ctx, name: str = "", **args: Any):
        payload = {k: v for k, v in args.items() if k != "name"}
        if ctx is not None:
            form = getattr(ctx, "form", None) or getattr(ctx, "data", None) or {}
            if isinstance(form, dict):
                for key, value in form.items():
                    if key not in payload and key != "name":
                        payload[str(key)] = value
        host.submit(str(name or ""), payload)
        return None

    host._wire = ch
    host._dispatch = dispatch
    host._region_uid = slot_uid
    cores = dict(host._cores or {})
    cores["channel"] = ch
    host._cores = cores
    return ch


def resolve_action_name(host: Any, action: Any) -> str:
    """Turn a bound method / @action function / string into a registered name.

    Product code prefers ``host.control(cart.add, id=sku)``. Strings stay as
    the escape hatch. Never imports Channel.
    """
    if isinstance(action, str):
        return action
    if not callable(action):
        raise DispatchError(f"control target is not an action: {type(action).__name__}")

    existing = getattr(action, "__ux_action__", None)
    if existing is not None and getattr(existing, "name", None):
        return str(existing.name)

    if inspect.ismethod(action):
        ident = getattr(action.__self__, "id", None)
        if ident:
            return f"{ident}.{action.__name__}"

    runtime = getattr(host, "runtime", None)
    if runtime is not None:
        target_func = getattr(action, "__func__", action)
        for spec in getattr(runtime, "actions", {}).values():
            fn = spec.fn
            if fn is action or getattr(fn, "__func__", fn) is target_func:
                return spec.name

    raise DispatchError("handler is not a registered Action")


def control_attrs(host: Any, action: Any, **args: Any) -> dict[str, str]:
    """Mint control attrs through the App façade.

    ``action`` may be a bound Component method, an ``@action`` function, or a
    string name (escape hatch). Live Channel when ``App.attach`` has run;
    otherwise the in-process Cap. Keys are underscore form for ux-dom.
    """
    name = resolve_action_name(host, action)
    wire = getattr(host, "_wire", None)
    dispatch = getattr(host, "_dispatch", None)
    if wire is not None and dispatch is not None:
        trust: dict[str, Any] = {"name": name}
        trust.update(args)
        return wire.control(dispatch, trust=trust).as_ux_dom()
    token = host.mint(name, args)
    return {
        "data_action": str(name),
        "data_cap": token,
        "data_args": json.dumps(args, sort_keys=True, separators=(",", ":"), default=str),
    }
