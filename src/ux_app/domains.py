"""Domain packs, stamp, structure. Same path for bundled and product packs."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Iterable

from ux_app.errors import DoctorError, IllegalOp
from ux_app.ops import S_PAIRS, fq_of, is_s_pair, validate_pair

Driver = Callable[[Any, Any], None]


@dataclass(frozen=True)
class DomainPack:
    name: str
    version: str
    seed_pairs: tuple[tuple[str, str], ...]
    driver_hint: str = ""
    core: bool = False
    driver: Driver | None = None

    @property
    def pairs(self) -> frozenset[tuple[str, str]]:
        return frozenset(self.seed_pairs)

    def major(self) -> str:
        return (self.version or "1").split(".", 1)[0]


BASELINE = DomainPack(
    name="baseline",
    version="1",
    seed_pairs=(("kv", "set"), ("kv", "delete"), ("log", "append")),
    driver_hint="kv+log",
    core=True,
)

UI = DomainPack(
    name="ui",
    version="1",
    seed_pairs=(("ui.dom", "morph"), ("ui.dom", "restore")),
    driver_hint="ui.dom",
    core=True,
)


def stdlib_dir() -> Path:
    return Path(__file__).resolve().parent / "stdlibs"


def load_bundled(name: str) -> DomainPack:
    path = stdlib_dir() / f"{name}.stdlib.json"
    if not path.is_file():
        raise IllegalOp(f"unknown bundled domain: {name}")
    data = json.loads(path.read_text(encoding="utf-8"))
    pairs = []
    for item in data.get("seed_pairs") or []:
        ns, n = item["ns"], item["name"]
        validate_pair(ns, n)
        pairs.append((ns, n))
    if not pairs:
        raise IllegalOp(f"stdlib {name} has no seed pairs")
    return DomainPack(
        name=data["name"],
        version=str(data.get("version") or "1"),
        seed_pairs=tuple(pairs),
        driver_hint=str(data.get("driver_hint") or name),
        core=False,
    )


class DomainTable:
    def __init__(self) -> None:
        self._packs: dict[str, DomainPack] = {
            "baseline": BASELINE,
            "ui": UI,
        }
        self._stamp: set[tuple[str, str]] = set(S_PAIRS)
        self._agreed: list[str] = ["baseline", "ui"]
        self._drivers: dict[tuple[str, str], Driver] = {}
        self._missing_drivers: set[tuple[str, str]] = set()

    @property
    def stamp(self) -> frozenset[tuple[str, str]]:
        return frozenset(self._stamp)

    @property
    def names(self) -> list[str]:
        return list(self._agreed)

    @property
    def packs(self) -> dict[str, DomainPack]:
        return dict(self._packs)

    @property
    def drivers(self) -> dict[tuple[str, str], Driver]:
        return dict(self._drivers)

    def register_pack(self, pack: DomainPack) -> None:
        if not pack.seed_pairs:
            raise IllegalOp(f"stdlib {pack.name} has no seed pairs")
        for ns, name in pack.seed_pairs:
            validate_pair(ns, name)
            if pack.core and not is_s_pair(ns, name):
                raise IllegalOp(f"core stdlib {pack.name} has undeclared pair {fq_of(ns, name)}")
        existing = self._packs.get(pack.name)
        if existing and existing.core and not pack.core:
            raise IllegalOp(f"cannot overwrite core stdlib {pack.name}")
        self._packs[pack.name] = pack

    def use(self, *names: str, peer_accepts: Iterable[str] | None = None) -> None:
        accepts = set(peer_accepts) if peer_accepts is not None else None
        for name in names:
            pack = self._packs.get(name)
            if pack is None:
                try:
                    pack = load_bundled(name)
                    self.register_pack(pack)
                except IllegalOp:
                    raise IllegalOp(f"unknown domain: {name}") from None
            if accepts is not None and name not in accepts and name != "baseline":
                continue
            if name not in self._agreed:
                self._agreed.append(name)
            self._stamp |= set(pack.seed_pairs)
            if pack.driver is not None:
                for pair in pack.seed_pairs:
                    if not is_s_pair(*pair):
                        self._drivers[pair] = pack.driver
                        self._missing_drivers.discard(pair)
            else:
                for pair in pack.seed_pairs:
                    if not is_s_pair(*pair) and pair not in self._drivers:
                        self._missing_drivers.add(pair)

    def register_driver(self, ns: str, name: str, fn: Driver) -> None:
        validate_pair(ns, name)
        self._drivers[(ns, name)] = fn
        self._missing_drivers.discard((ns, name))

    def undriven(self) -> list[tuple[str, str]]:
        return sorted(self._missing_drivers)

    def doctor_issues(self) -> list[str]:
        issues: list[str] = []
        for ns, name in sorted(self._stamp):
            if "." in name:
                issues.append(f"pair {fq_of(ns, name)} has a dotted name")
            if not is_s_pair(ns, name) and (ns, name) not in self._drivers:
                issues.append(f"stamped pair {fq_of(ns, name)} has no driver")
        return issues


def default_table() -> DomainTable:
    table = DomainTable()
    table.use("baseline", "ui")
    return table
