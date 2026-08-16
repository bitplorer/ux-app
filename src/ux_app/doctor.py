"""Doctor checks. Isolation, stamp, drivers, planes, production profile."""

from __future__ import annotations

from typing import Any

from ux_app.errors import DoctorError
from ux_app.isolation import scan_imports, scan_public_names
from ux_app.state import is_money_shaped

PRODUCTION = frozenset({"production", "production-v1"})


def inspect_package() -> list[str]:
    issues: list[str] = []
    issues.extend(scan_imports())
    banned = scan_public_names()
    for name in banned:
        issues.append(f"banned public name: {name}")
    return issues


def inspect_app(app: Any) -> list[str]:
    issues = inspect_package()
    runtime = getattr(app, "runtime", None)
    if runtime is None:
        issues.append("app has no runtime")
        return issues
    domains = getattr(runtime, "domains", None)
    if domains is not None:
        issues.extend(domains.doctor_issues())
    allow = set(getattr(runtime, "client_state", ()) or ())
    for inst in getattr(runtime, "components", {}).values():
        specs = getattr(inst, "field_specs", {}) or {}
        for spec in specs.values():
            if spec.plane != "client":
                continue
            key = spec.allowlist_key or spec.name
            if is_money_shaped(spec.name) or is_money_shaped(key):
                issues.append(
                    f"money-shaped field {spec.name!r} must not be on the client plane"
                )
            if key not in allow:
                issues.append(f"client key {key!r} is not on the allowlist")
    profile = getattr(runtime, "profile", "") or getattr(app, "profile", "")
    if profile in PRODUCTION:
        once = getattr(getattr(runtime, "caps", None), "once", None)
        if once is None or not getattr(once, "durable", False):
            issues.append("production profile requires a durable once-store")
        if not getattr(runtime, "receipts", False) and not getattr(app, "receipts", False):
            issues.append("production profile requires receipts")
    return issues


def run(app: Any | None = None, *, fail: bool = False) -> list[str]:
    issues = inspect_app(app) if app is not None else inspect_package()
    if fail and issues:
        raise DoctorError(issues)
    return issues
