"""Doctor UI health — undriven UI pairs + missing declared runtimes.

Does not import ux_channel or cek_*. Composite runtime map is duplicated
here so ux-app doctor stays green without ux-dom installed.
"""

from __future__ import annotations

from typing import Any

from ux_app.doctor import PRODUCTION

# Composite stem → required Document.use runtime (None = pure HTML).
COMPOSITE_RUNTIMES: dict[str, str | None] = {
    "tabs": "alpine",
    "dialog": "alpine",
    "carousel": "alpine",
    "toast": None,
    "datepicker": None,
    "chart": None,
    "slider": None,
    "table": None,
    "button": None,
}


def doctor_ui_health(app: Any) -> list[str]:
    """Return issues for missing declared runtimes.

    Undeclared runtimes fail only under a production profile so
    ``App.bind()`` / ``doctor --fail`` stay incremental on the ui profile.
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
    for name in getattr(runtime, "required_composites", ()) or ():
        need = COMPOSITE_RUNTIMES.get(str(name).lower())
        if need:
            required.add(need)
    for rt in sorted(required - declared):
        issues.append(f"composite requires undeclared runtime {rt!r}")
    return issues
