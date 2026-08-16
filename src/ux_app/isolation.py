"""Mechanical isolation. No Channel / CEK imports."""

from __future__ import annotations

import ast
from pathlib import Path
from typing import Iterable

FORBIDDEN_PREFIXES = ("ux_channel", "cek_host", "cek_surface", "cek_")

BANNED_PUBLIC_NAMES = frozenset(
    {
        "chrome",
        "chrome_pending",
        "chrome_shadow",
        "arm",
        "reply",
        "Reply",
        "Effect",
        "KNOWN_KINDS",
        "Partial",
        "shell",
        "Frame",
        "Main",
        "ceremony",
        "Interactive",
        "controls",
        "ActionResult",
        "Surface",
        "VStack",
        "HStack",
        "command",
    }
)


def _is_forbidden_module(name: str | None) -> bool:
    if not name:
        return False
    root = name.split(".", 1)[0]
    if root in {"ux_channel", "cek_host", "cek_surface"}:
        return True
    if root.startswith("cek_"):
        return True
    return False


def package_root() -> Path:
    return Path(__file__).resolve().parent


def scan_imports(root: Path | None = None) -> list[str]:
    """Return violations: non-adapter modules that import Channel / CEK."""
    root = root or package_root()
    hits: list[str] = []
    for path in sorted(root.rglob("*.py")):
        rel = path.relative_to(root)
        parts = rel.parts
        if parts and parts[0] == "adapter":
            continue
        try:
            source = path.read_text(encoding="utf-8")
            tree = ast.parse(source, filename=str(path))
        except (OSError, SyntaxError) as exc:
            hits.append(f"{rel}: unreadable ({exc})")
            continue
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    if _is_forbidden_module(alias.name):
                        hits.append(f"{rel}:{node.lineno} import {alias.name}")
            elif isinstance(node, ast.ImportFrom):
                if _is_forbidden_module(node.module):
                    hits.append(f"{rel}:{node.lineno} from {node.module} import …")
    return hits


def scan_public_names(names: Iterable[str] | None = None) -> list[str]:
    if names is None:
        from ux_app import __all__ as exported

        names = exported
    return [n for n in names if n in BANNED_PUBLIC_NAMES]
