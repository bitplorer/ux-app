"""Doctor UI health — undriven UI pairs + missing declared runtimes.

Does not import ux_channel or cek_*. Composite runtime map is duplicated
here so ux-app doctor stays green without ux-dom installed.
"""

from __future__ import annotations

from typing import Any

from ux_app.doctor import PRODUCTION

# Elevated chrome is Channel-first. Alpine is last-resort perception only.
CHANNEL_FIRST_COMPOSITES: frozenset[str] = frozenset(
    {
        "tabs",
        "dialog",
        "sheet",
        "carousel",
        "command",
        "popover",
        "dropdown_menu",
    }
)

# Composite stem → required Document.use runtime (None = Channel-first / HTML).
COMPOSITE_RUNTIMES: dict[str, str | None] = {
    "tabs": None,
    "dialog": None,
    "sheet": None,
    "carousel": None,
    "command": None,
    "popover": None,
    "dropdown_menu": None,
    "toast": None,
    "datepicker": None,
    "chart": None,
    "slider": None,
    "table": None,
    "button": None,
}


def doctor_ui_health(app: Any) -> list[str]:
    """Return issues for missing declared runtimes and alpine-for-open.

    Undeclared runtimes fail only under a production profile so
    ``App.bind()`` / ``doctor --fail`` stay incremental on the ui profile.

    Alpine-for-open fails when a Channel path exists (elevated Dialog/Tabs/…).
    """
    issues: list[str] = []
    runtime = getattr(app, "runtime", None)
    if runtime is None:
        return issues
    profile = getattr(runtime, "profile", "") or getattr(app, "profile", "")
    if profile not in PRODUCTION:
        return issues
    declared = set(getattr(runtime, "declared_runtimes", ()) or ())
    required: set[str] = set(getattr(runtime, "required_runtimes", ()) or ())
    overrides = getattr(runtime, "composite_runtimes", None) or {}
    for name in getattr(runtime, "required_composites", ()) or ():
        key = str(name).lower()
        claimed = overrides.get(key, COMPOSITE_RUNTIMES.get(key))
        if key in CHANNEL_FIRST_COMPOSITES and claimed == "alpine":
            issues.append(
                f"alpine-for-open is forbidden for {key!r} (Channel path exists)"
            )
            continue
        if claimed:
            required.add(claimed)
    for rt in sorted(required - declared):
        issues.append(f"composite requires undeclared runtime {rt!r}")
    return issues
