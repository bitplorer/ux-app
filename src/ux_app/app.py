"""App — composition root. Boot Document + Channel + default domains."""

from __future__ import annotations

import html
import inspect
from typing import Any, Callable, Iterable

from ux_app.adapter.boot import KERNEL_SCRIPT, PREVIEW_SCRIPT, SCRIPT_ORDER, try_boot
from ux_app.adapter.runtime import LocalRuntime
from ux_app.component import is_component
from ux_app.context import Principal
from ux_app.doctor import PRODUCTION, inspect_app, run as run_doctor
from ux_app.domains import DomainPack, DomainTable, default_table
from ux_app.errors import DispatchError, IllegalOp, ValidationError
from ux_app.layout import Layout, default_layout
from ux_app.ops import is_s_pair
from ux_app.result import Result
from ux_app.state import is_money_shaped

_DEFAULT_CLIENT = ("ui.theme", "ui.density")


class App:
    """Host-authored application. Authors do not mention Intent or CapService."""

    def __init__(
        self,
        runtime: LocalRuntime,
        *,
        title: str = "App",
        cek: str = "off",
        layout: Layout | None = None,
        cores: Any = None,
        strict: bool = True,
    ) -> None:
        self.runtime = runtime
        runtime.app = self
        self.title = title
        self.cek = cek
        self.layout = layout or default_layout()
        self.session: dict[str, Any] = {}
        self.store: dict[str, Any] = {}
        self._cores = cores
        self.strict = strict
        self.scripts = SCRIPT_ORDER
        if strict:
            issues = inspect_app(self)
            # Isolation / banned names fail closed at boot. Domain driver
            # misses stay visible via doctor() so use() can be incremental.
            hard = [i for i in issues if not i.startswith("stamped pair ")]
            if hard:
                from ux_app.errors import DoctorError

                raise DoctorError(hard)

    @classmethod
    def bind(
        cls,
        document: Any = None,
        channel: Any = None,
        *,
        title: str = "App",
        cek: str = "off",
        domains: DomainTable | None = None,
        profile: str = "ui",
        client_state: tuple[str, ...] = _DEFAULT_CLIENT,
        secret: str | None = None,
        require_cap: bool = True,
        strict: bool = True,
    ) -> "App":
        """In-process Host+Peer. Used by tests and hosts that already have cores."""
        table = domains or default_table()
        receipts = profile in PRODUCTION
        runtime = LocalRuntime(
            secret=secret,
            domains=table,
            profile=profile,
            client_state=client_state,
            require_cap=require_cap,
            receipts=receipts,
        )
        if receipts:
            runtime.caps.once.durable = True
        cores = None
        if document is not None or channel is not None:
            cores = {"document": document, "channel": channel}
        return cls(runtime, title=title, cek=cek, cores=cores, strict=strict)

    @classmethod
    def boot(
        cls,
        title: str = "App",
        *,
        cek: str = "off",
        domains: tuple[str, ...] = ("baseline", "ui"),
        profile: str = "ui",
        client_state: tuple[str, ...] = _DEFAULT_CLIENT,
        secret: str | None = None,
        strict: bool = True,
    ) -> "App":
        """Stand up Document + Channel when present; else LocalRuntime.

        Always injects Peer-kernel then preview script tags.
        Always maintains a session pair set (even when cek=off).
        """
        cores = try_boot(title, cek=cek, profile=profile)
        app = cls.bind(
            document=cores.document,
            channel=cores.channel,
            title=title,
            cek=cek,
            profile=profile,
            client_state=client_state,
            secret=secret,
            strict=strict,
        )
        extra = [n for n in domains if n not in {"baseline", "ui"}]
        if extra:
            app.use(*extra)
        return app

    # -- registry --------------------------------------------------------

    def add(self, spec: Any) -> Any:
        """Register a Component (class or instance). Alias of register."""
        return self.register(spec)

    def register(self, spec: Any) -> Any:
        inst = self.runtime.register_component(spec)
        if hasattr(inst, "bind_app"):
            inst.bind_app(self)
        self._gate_planes(inst)
        return inst

    def _gate_planes(self, inst: Any) -> None:
        allow = set(self.runtime.client_state)
        specs = getattr(inst, "field_specs", {}) or {}
        for spec in specs.values():
            if spec.plane != "client":
                continue
            key = spec.allowlist_key or spec.name
            if is_money_shaped(spec.name) or is_money_shaped(key):
                raise ValidationError(
                    f"money-shaped field {spec.name!r} must not be on the client plane",
                    fields={spec.name: "client"},
                )
            if key not in allow:
                raise ValidationError(
                    f"client key {key!r} is not on the allowlist",
                    fields={spec.name: "allowlist"},
                )

    # -- domains ---------------------------------------------------------

    def use(self, *names: str, driver: Callable[..., Any] | None = None) -> "App":
        """Load bundled stdlibs, agree, stamp. Driver required for extensions."""
        self.runtime.domains.use(*names)
        if driver is not None:
            for name in names:
                pack = self.runtime.domains.packs.get(name)
                if pack is None:
                    continue
                for pair in pack.seed_pairs:
                    if is_s_pair(*pair):
                        continue
                    self.runtime.peer.register_driver(pair[0], pair[1], driver)
                    self.runtime.domains.register_driver(pair[0], pair[1], driver)
        return self

    def domain(
        self,
        name: str,
        version: str,
        pairs: Iterable[tuple[str, str]],
        driver: Callable[..., Any] | None = None,
    ) -> "App":
        seed = tuple(pairs)
        pack = DomainPack(
            name=name,
            version=version,
            seed_pairs=seed,
            driver_hint=name,
            driver=driver,
        )
        self.runtime.domains.register_pack(pack)
        self.runtime.domains.use(name)
        if driver is not None:
            for ns, n in seed:
                if is_s_pair(ns, n):
                    continue
                self.runtime.peer.register_driver(ns, n, driver)
                self.runtime.domains.register_driver(ns, n, driver)
        return self

    def drive(self, name: str, fn: Callable[..., Any]) -> "App":
        pack = self.runtime.domains.packs.get(name)
        if pack is None:
            raise IllegalOp(f"unknown domain: {name}")
        for ns, n in pack.seed_pairs:
            if is_s_pair(ns, n):
                continue
            self.runtime.peer.register_driver(ns, n, fn)
            self.runtime.domains.register_driver(ns, n, fn)
        return self

    def declare_runtime(self, *names: str) -> "App":
        """Record Document.use plugins (alpine, xelement, …) for doctor UI health."""
        current = set(self.runtime.declared_runtimes)
        current.update(n.strip().lower() for n in names if n)
        self.runtime.declared_runtimes = frozenset(current)
        return self

    def require_composite(self, *names: str) -> "App":
        """Tell doctor which kit composites this app actually uses."""
        current = set(self.runtime.required_composites)
        current.update(n.strip().lower() for n in names if n)
        self.runtime.required_composites = frozenset(current)
        needed = set(self.runtime.required_runtimes)
        from ux_app.ui_health import COMPOSITE_RUNTIMES

        for name in names:
            rt = COMPOSITE_RUNTIMES.get(str(name).strip().lower())
            if rt:
                needed.add(rt)
        self.runtime.required_runtimes = frozenset(needed)
        return self

    # -- submit / click / emit -------------------------------------------

    def submit(
        self,
        action: str,
        args: dict[str, Any] | None = None,
        *,
        cap: str | None = None,
        principal: Principal | None = None,
    ) -> Result:
        return self.runtime.submit(action, args, cap=cap, principal=principal)

    async def async_submit(
        self,
        action: str,
        args: dict[str, Any] | None = None,
        *,
        cap: str | None = None,
        principal: Principal | None = None,
    ) -> Result:
        return await self.runtime.async_submit(
            action, args, cap=cap, principal=principal
        )

    def mint(self, action: str, args: dict[str, Any] | None = None) -> str:
        return self.runtime.caps.mint(action, args)

    def attach(self, asgi: Any, **kwargs: Any) -> Any:
        """Mount the live Channel behind this App.

        Idempotent. No-op (returns None) when ux-channel is not installed
        or ``asgi`` is None. Product code never imports the Channel.
        """
        from ux_app.adapter.channel import attach as attach_wire

        return attach_wire(self, asgi, **kwargs)

    def region(self, render: Any, *, uid: str | None = None) -> "App":
        """Hand a host render to Channel's Region API (via the adapter).

        Does not invent a second slot type. Channel already owns
        ``@ch.region`` / ``ch.use`` / ``Region.mount``. This method only
        stores the callback so product code never imports ux_channel.
        Default uid is ``app.root``.
        """
        self._region_render = render
        if uid:
            self._region_uid = uid
        return self

    @property
    def region_uid(self) -> str:
        from ux_app.adapter.channel import DEFAULT_REGION_UID

        return getattr(self, "_region_uid", None) or DEFAULT_REGION_UID

    @property
    def state(self) -> Any:
        """Live Channel state bag after attach(); None offline / in tests.

        Product code prefers Component Session/Client fields. This property
        is the adapter/test escape hatch — not the day-1 author API.
        """
        return getattr(self, "_state", None)

    def control(self, action: str, **args: Any) -> dict[str, str]:
        """Mint signed control attrs. Live Channel after attach(); else in-process Cap."""
        from ux_app.adapter.channel import control_attrs

        return control_attrs(self, action, **args)

    def click(self, ident: str, method: str | None = None, **args: Any) -> Result:
        """Test helper: mint the control Cap and submit the Component method."""
        spec = self._resolve_click(ident, method)
        bound = {}
        for pname, param in spec.params.items():
            if pname in {"ctx", "self", "cls"}:
                continue
            if param.default is not inspect.Parameter.empty:
                bound[pname] = param.default
        bound.update(args)
        cap = self.runtime.caps.mint(spec.name, bound)
        return self.submit(spec.name, bound, cap=cap)

    def _resolve_click(self, ident: str, method: str | None):
        if ident not in self.runtime.components:
            raise DispatchError(f"unknown component {ident!r}")
        if method:
            name = f"{ident}.{method}"
            spec = self.runtime.actions.get(name)
            if spec is None:
                raise DispatchError(f"unknown action {name!r}")
            return spec
        matches = [
            s
            for s in self.runtime.actions.values()
            if s.component_id == ident and s.method
        ]
        if not matches:
            raise DispatchError(f"no Action on component {ident!r}")
        preferred = [s for s in matches if s.method in {"add", "click", "increment", "inc"}]
        return (preferred or matches)[0]

    def emit(
        self, event: str, slots: dict[str, Any] | None = None, *, cap: str | None = None
    ) -> Result:
        return self.runtime.emit(event, slots, cap=cap)

    # -- render ----------------------------------------------------------

    def html(self, ident: str) -> str:
        return self.runtime.render_component(ident)

    def page(self) -> str:
        """Empty-or-filled page with kernel then preview scripts."""
        parts: list[str] = []
        for inst in self.runtime.components.values():
            ident = html.escape(str(inst.id), quote=True)
            parts.append(f'<div id="{ident}">{self.html(inst.id)}</div>')
        content = "".join(parts)
        notices = self.world.ui.get("notices", "")
        if not isinstance(notices, str):
            notices = html.escape(str(notices))
        title = html.escape(self.title)
        kernel_src, kernel_role = SCRIPT_ORDER[0]
        preview_src, preview_role = SCRIPT_ORDER[1]
        return (
            "<!doctype html>\n<html>\n<head>\n"
            f"<title>{title}</title>\n"
            f'<script src="{kernel_src}" data-role="{kernel_role}"></script>\n'
            f'<script src="{preview_src}" data-role="{preview_role}"></script>\n'
            "</head>\n<body>\n"
            f'<div id="content">{content}</div>\n'
            f'<div id="notices">{notices}</div>\n'
            "</body>\n</html>\n"
        )

    # -- inspect ---------------------------------------------------------

    @property
    def world(self) -> Any:
        return self.runtime.peer.world

    @property
    def stamp(self) -> frozenset[tuple[str, str]]:
        return self.runtime.domains.stamp

    @property
    def profile(self) -> str:
        return self.runtime.profile

    @property
    def receipts(self) -> bool:
        return bool(self.runtime.receipts)

    def doctor(self, *, fail: bool = False) -> list[str]:
        return run_doctor(self, fail=fail)

    def explain(self) -> dict[str, Any]:
        domains = self.runtime.domains
        return {
            "title": self.title,
            "cek": self.cek,
            "profile": self.profile,
            "actions": sorted(self.runtime.actions),
            "components": sorted(self.runtime.components),
            "domains": list(domains.names),
            "stamp": sorted(f"{ns}.{name}" for ns, name in domains.stamp),
            "drivers": sorted(f"{ns}.{name}" for ns, name in domains.drivers),
            "undriven": [f"{ns}.{name}" for ns, name in domains.undriven()],
            "scripts": [src for src, _ in self.scripts],
        }

    def shutdown(self) -> None:
        self.layout.dispose()


# Re-export attach helpers used by tests that want the script constants.
KERNEL = KERNEL_SCRIPT
PREVIEW = PREVIEW_SCRIPT
