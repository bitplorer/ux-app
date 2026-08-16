"""Peer apply + default S drivers. No mint. No Channel import at module level."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable

from ux_app.drivers import search_driver
from ux_app.ops import Op, is_s_pair
from ux_app.preview import preview

Driver = Callable[[Op, "World"], None]


@dataclass
class World:
    kv: dict[str, Any] = field(default_factory=dict)
    log: list[dict[str, Any]] = field(default_factory=list)
    ui: dict[str, Any] = field(default_factory=dict)


def _kv_set(op: Op, world: World) -> None:
    key = op.payload.get("key")
    if not key:
        raise ValueError("kv.set missing key")
    world.kv[str(key)] = op.payload.get("value")


def _kv_delete(op: Op, world: World) -> None:
    key = op.payload.get("key")
    if not key:
        raise ValueError("kv.delete missing key")
    world.kv.pop(str(key), None)


def _log_append(op: Op, world: World) -> None:
    message = op.payload.get("message")
    if not isinstance(message, str):
        raise ValueError("log.append missing message")
    world.log.append(dict(op.payload))


def _ui_morph(op: Op, world: World) -> None:
    target = op.payload.get("target")
    if not target:
        raise ValueError("ui.dom.morph missing target")
    world.ui[str(target)] = op.payload.get("patch")


def _ui_restore(op: Op, world: World) -> None:
    target = op.payload.get("target")
    if not target:
        raise ValueError("ui.dom.restore missing target")
    world.ui[str(target)] = op.payload.get("snapshot")


S_DRIVERS: dict[tuple[str, str], Driver] = {
    ("kv", "set"): _kv_set,
    ("kv", "delete"): _kv_delete,
    ("log", "append"): _log_append,
    ("ui.dom", "morph"): _ui_morph,
    ("ui.dom", "restore"): _ui_restore,
}


@dataclass
class PeerRuntime:
    world: World = field(default_factory=World)
    drivers: dict[tuple[str, str], Driver] = field(default_factory=lambda: dict(S_DRIVERS))
    unknown: str = "strict"
    last_failed: list[str] = field(default_factory=list)
    last_landed: list[str] = field(default_factory=list)
    receipts: bool = False

    def register_driver(self, ns: str, name: str, fn: Driver) -> None:
        self.drivers[(ns, name)] = fn

    def apply(self, ops: list[Op], *, clear_preview: bool = True) -> None:
        if clear_preview:
            preview.clear()
        self.last_failed = []
        self.last_landed = []
        if self.unknown == "strict":
            for op in ops:
                if op.pair not in self.drivers and not is_s_pair(*op.pair):
                    self.last_failed = [o.fq for o in ops]
                    raise ValueError(f"no driver for {op.fq}")
        snapshot_kv = dict(self.world.kv)
        snapshot_ui = dict(self.world.ui)
        snapshot_log = list(self.world.log)
        try:
            for op in ops:
                fn = self.drivers.get(op.pair)
                if fn is None:
                    if self.unknown == "strict":
                        raise ValueError(f"no driver for {op.fq}")
                    self.last_failed.append(op.fq)
                    continue
                fn(op, self.world)
                self.last_landed.append(op.fq)
        except Exception:
            self.world.kv = snapshot_kv
            self.world.ui = snapshot_ui
            self.world.log = snapshot_log
            raise


__all__ = ["World", "PeerRuntime", "S_DRIVERS", "search_driver"]
