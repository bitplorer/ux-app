"""In-process Host + Peer for bind() and tests.

Not a third kernel. Does not import ux_channel or cek_*.
Obeys: verify before compose, refuse → ops [], pair identity, two clocks.
"""

from __future__ import annotations

import inspect
import json
from typing import Any

from ux_app.action import ActionSpec, all_actions, get_action, validate_args
from ux_app.adapter.caps import CapError, CapMachine
from ux_app.adapter.peer import PeerRuntime
from ux_app.component import is_component
from ux_app.context import ActionContext, Principal
from ux_app.domains import DomainTable
from ux_app.drivers import search_driver
from ux_app.errors import DispatchError, IllegalOp, ValidationError
from ux_app.ops import Op, as_ops, check_stamp, is_s_pair, update
from ux_app.preview import preview
from ux_app.result import Result, authority_refusal, dispatch_error, ok


def _defaults_for(spec: ActionSpec) -> dict[str, Any]:
    args: dict[str, Any] = {}
    for pname, param in spec.params.items():
        if pname in {"ctx", "self", "cls"}:
            continue
        if param.default is not inspect.Parameter.empty:
            args[pname] = param.default
    return args


class LocalRuntime:
    def __init__(
        self,
        *,
        secret: str | None = None,
        domains: DomainTable,
        profile: str = "ui",
        client_state: tuple[str, ...] = ("ui.theme", "ui.density"),
        require_cap: bool = True,
        receipts: bool = False,
    ) -> None:
        self.caps = CapMachine(secret)
        self.peer = PeerRuntime(receipts=receipts)
        self.domains = domains
        self.profile = profile
        self.client_state = tuple(client_state)
        self.require_cap = require_cap
        self.receipts = receipts
        self.continuations: dict[str, Any] = {}
        self.components: dict[str, Any] = {}
        self.actions: dict[str, ActionSpec] = {}
        self.app: Any = None
        self.declared_runtimes: frozenset[str] = frozenset()
        self.required_runtimes: frozenset[str] = frozenset()
        self.required_composites: frozenset[str] = frozenset()
        self._refresh_actions()

    def _refresh_actions(self) -> None:
        self.actions.update(all_actions())

    def register_component(self, spec: Any) -> Any:
        inst = spec() if isinstance(spec, type) else spec
        if not is_component(inst):
            raise DispatchError("not a Component (need id + render)")
        ident = str(inst.id)
        self.components[ident] = inst
        self._register_methods(inst)
        return inst

    def _register_methods(self, inst: Any) -> None:
        for name, member in inspect.getmembers(inst, predicate=inspect.ismethod):
            if name.startswith("_") or name in {
                "render",
                "to_html",
                "bind_app",
                "clear_dirty",
                "is_dirty",
            }:
                continue
            existing = getattr(member, "__ux_action__", None)
            action_name = existing.name if existing else f"{inst.id}.{name}"
            if action_name in self.actions and existing is None:
                continue
            spec = existing or ActionSpec(
                name=action_name,
                fn=member,
                caps=(),
                component_id=str(inst.id),
                method=name,
                public=True,
                is_async=inspect.iscoroutinefunction(member.__func__),
                params=dict(inspect.signature(member).parameters),
            )
            if existing:
                spec.component_id = str(inst.id)
                spec.method = name
                spec.fn = member
            self.actions[action_name] = spec

    def mint_control(
        self, handler: Any, extra_args: dict[str, Any] | None = None
    ) -> dict[str, str]:
        spec = self._spec_for_handler(handler)
        args = _defaults_for(spec)
        args.update(extra_args or {})
        token = self.caps.mint(spec.name, args)
        return {
            "data-action": spec.name,
            "data-cap": token,
            "data-args": json.dumps(args, sort_keys=True, separators=(",", ":")),
        }

    def _spec_for_handler(self, handler: Any) -> ActionSpec:
        existing = getattr(handler, "__ux_action__", None)
        if existing:
            return self.actions.get(existing.name) or existing
        if inspect.ismethod(handler):
            owner = handler.__self__
            ident = getattr(owner, "id", None)
            if ident:
                name = f"{ident}.{handler.__name__}"
                spec = self.actions.get(name)
                if spec:
                    return spec
        raise DispatchError("handler is not a registered Action")

    def render_component(self, ident: str) -> str:
        inst = self.components[ident]
        html = (
            inst.to_html(mint=self.mint_control)
            if hasattr(inst, "to_html")
            else str(inst.render())
        )
        self.peer.world.ui[ident] = html
        return html

    def submit(
        self,
        action: str,
        args: dict[str, Any] | None = None,
        *,
        cap: str | None = None,
        principal: Principal | None = None,
        _trusted: bool = False,
    ) -> Result:
        self._refresh_actions()
        args = dict(args or {})
        spec = self.actions.get(action) or get_action(action)
        if spec is None:
            return dispatch_error(f"unknown action {action!r}")
        # Present Cap always verifies. Public + no cap is the only skip.
        # _trusted is Host-only: emit() already verified the continuation Cap
        # against the sealed args, then fills declared slots.
        if not _trusted and (cap is not None or not spec.public):
            try:
                self.caps.verify(cap, action, args)
            except CapError as exc:
                return authority_refusal(exc.reason)

        if spec.is_async:
            return dispatch_error("async action: use async_submit")

        try:
            clean = validate_args(spec, args)
        except ValidationError as exc:
            morphs = [
                Op.ui_morph(f"{action}.{field}-error", {"text": msg})
                for field, msg in exc.fields.items()
            ]
            return Result(ok=False, ops=morphs, kind="validation", error=str(exc))

        ctx = ActionContext(
            app=getattr(self, "app", None),
            action=action,
            args=clean,
            principal=principal or Principal(),
        )
        inst = self.components.get(spec.component_id) if spec.component_id else None
        try:
            returned = self._call(spec, ctx, clean, inst)
        except ValidationError as exc:
            morphs = [
                Op.ui_morph(f"{action}.{field}-error", {"text": msg})
                for field, msg in exc.fields.items()
            ]
            return Result(ok=False, ops=morphs, kind="validation", error=str(exc))
        except IllegalOp as exc:
            return dispatch_error(str(exc))

        return self._finish(returned, inst, ctx)

    async def async_submit(
        self,
        action: str,
        args: dict[str, Any] | None = None,
        *,
        cap: str | None = None,
        principal: Principal | None = None,
    ) -> Result:
        self._refresh_actions()
        spec = self.actions.get(action) or get_action(action)
        if spec is None:
            return dispatch_error(f"unknown action {action!r}")
        if not spec.is_async:
            return self.submit(action, args, cap=cap, principal=principal)
        args = dict(args or {})
        if cap is not None or not spec.public:
            try:
                self.caps.verify(cap, action, args)
            except CapError as exc:
                return authority_refusal(exc.reason)
        try:
            clean = validate_args(spec, args)
        except ValidationError as exc:
            return Result(ok=False, ops=[], kind="validation", error=str(exc))
        ctx = ActionContext(
            app=getattr(self, "app", None),
            action=action,
            args=clean,
            principal=principal or Principal(),
        )
        inst = self.components.get(spec.component_id) if spec.component_id else None
        returned = await self._call_async(spec, ctx, clean, inst)
        return self._finish(returned, inst, ctx)

    def _finish(self, returned: Any, inst: Any, ctx: ActionContext) -> Result:
        try:
            ops = as_ops(returned)
        except IllegalOp as exc:
            return dispatch_error(str(exc))

        if returned is None and inst is not None and getattr(inst, "is_dirty", lambda: False)():
            ops = [update(str(inst.id))]

        stamped: list[Op] = []
        try:
            for op in ops:
                if is_s_pair(*op.pair):
                    stamped.append(op)
                    continue
                stamped.append(Op.stamped(op.ns, op.name, op.payload, self.domains.stamp))
            check_stamp(stamped, self.domains.stamp)
        except IllegalOp as exc:
            return dispatch_error(str(exc))

        for item in ctx.continuations:
            item.cap = self.caps.mint(item.action, item.args)
            self.continuations[item.event] = item

        try:
            preview.clear()
            for op in stamped:
                if op.pair == ("ui.dom", "morph") and op.payload.get("patch") is None:
                    target = op.payload.get("target")
                    if target in self.components:
                        op.payload["patch"] = self.components[target].to_html(
                            mint=self.mint_control
                        )
                        if hasattr(self.components[target], "clear_dirty"):
                            self.components[target].clear_dirty()
            self.peer.apply(stamped, clear_preview=False)
        except Exception as exc:
            return dispatch_error(str(exc))

        meta: dict[str, Any] = {}
        if self.receipts:
            meta["receipt"] = {
                "landed": list(self.peer.last_landed),
                "failed": list(self.peer.last_failed),
            }
        return ok(stamped, **meta)

    def _call(self, spec: ActionSpec, ctx: ActionContext, args: dict[str, Any], inst: Any) -> Any:
        fn = spec.fn
        params = spec.params
        kwargs: dict[str, Any] = {}
        if "ctx" in params:
            kwargs["ctx"] = ctx
        for key, value in args.items():
            if key in params:
                kwargs[key] = value
        return fn(**kwargs) if kwargs or not args else fn()

    async def _call_async(
        self, spec: ActionSpec, ctx: ActionContext, args: dict[str, Any], inst: Any
    ) -> Any:
        fn = spec.fn
        params = spec.params
        kwargs: dict[str, Any] = {}
        if "ctx" in params:
            kwargs["ctx"] = ctx
        for key, value in args.items():
            if key in params:
                kwargs[key] = value
        return await fn(**kwargs)

    def emit(
        self, event: str, slots: dict[str, Any] | None = None, *, cap: str | None = None
    ) -> Result:
        cont = self.continuations.get(event)
        if cont is None:
            return authority_refusal("no follow-up for event")
        if not cap:
            return authority_refusal("follow-up requires Host-issued Cap")
        try:
            self.caps.verify(cap, cont.action, dict(cont.args))
        except CapError as exc:
            return authority_refusal(exc.reason)
        resolved = dict(cont.args)
        slots = dict(slots or {})
        for dest, src in cont.args_from.items():
            if src in slots:
                resolved[dest] = slots[src]
            elif src.startswith("store:") or src.startswith("search."):
                key = src.split(":", 1)[-1] if src.startswith("store:") else src
                if key in self.peer.world.kv:
                    resolved[dest] = self.peer.world.kv[key]
        return self.submit(cont.action, resolved, _trusted=True)

    def attach_search_driver(self) -> None:
        self.peer.register_driver("search", "hits", search_driver)
        self.peer.register_driver("search", "clear", search_driver)
        self.domains.register_driver("search", "hits", search_driver)
        self.domains.register_driver("search", "clear", search_driver)

    def attach_effects_driver(self) -> None:
        from ux_app.effects import effects_driver

        self.peer.register_driver("ui.notice", "push", effects_driver)
        self.peer.register_driver("ui.notice", "clear", effects_driver)
        self.domains.register_driver("ui.notice", "push", effects_driver)
        self.domains.register_driver("ui.notice", "clear", effects_driver)
