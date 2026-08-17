from __future__ import annotations

import ux_app
from ux_app.isolation import BANNED_PUBLIC_NAMES, scan_public_names


def test_all_is_small_and_named():
    expected = {
        "App",
        "Component",
        "action",
        "update",
        "notify",
        "go",
        "Op",
        "follow_up",
        "preview",
        "Client",
        "Session",
        "Store",
        "Transient",
        "Sealed",
        "Badge",
        "__version__",
        "open_overlay",
        "close_overlay",
        "select_region",
        "confirm",
        "form_result",
    }
    assert set(ux_app.__all__) == expected


def test_no_banned_names_in_all():
    assert scan_public_names(ux_app.__all__) == []
    for name in BANNED_PUBLIC_NAMES:
        assert name not in ux_app.__all__
        assert not hasattr(ux_app, name) or name in {"preview"}


def test_leftover_names_absent_from_docs():
    from pathlib import Path

    root = Path(__file__).resolve().parents[1]
    docs = [
        root / "README.md",
        root / "START.md",
        root / "ARCHITECTURE.md",
        root / "DOMAINS.md",
        root / "examples" / "cart.py",
    ]
    leftovers = ("chrome_pending", "chrome_shadow", "ActionResult", "KNOWN_KINDS")
    for path in docs:
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        for word in leftovers:
            assert word not in text, f"{path} contains {word}"
