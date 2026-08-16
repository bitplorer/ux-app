"""C-pre-03, C-pre-04 — isolation and cold import."""

from __future__ import annotations

import ast
import sys
from pathlib import Path

from ux_app.isolation import scan_imports, scan_public_names


def test_package_has_no_channel_imports_outside_adapter():
    assert scan_imports() == []


def test_scan_detects_leak_in_temp_tree(tmp_path: Path):
    (tmp_path / "ops.py").write_text("import ux_channel\n", encoding="utf-8")
    (tmp_path / "adapter").mkdir()
    (tmp_path / "adapter" / "ok.py").write_text("import ux_channel\n", encoding="utf-8")
    hits = scan_imports(tmp_path)
    assert any("ops.py" in h for h in hits)
    assert not any("adapter" in h for h in hits)


def test_scan_detects_cek_from_import(tmp_path: Path):
    (tmp_path / "app.py").write_text("from cek_host import Host\n", encoding="utf-8")
    hits = scan_imports(tmp_path)
    assert hits


def test_cold_import_does_not_load_channel_or_cek():
    banned = {"ux_channel", "cek_host", "cek_surface", "cek_runtime"}
    loaded = banned & set(sys.modules)
    assert not loaded
    import ux_app  # noqa: F401

    loaded = banned & set(sys.modules)
    assert not loaded


def test_public_all_has_no_banned_names():
    import ux_app

    assert scan_public_names(ux_app.__all__) == []


def test_adapter_is_allowed_to_mention_channel():
    boot = Path(__file__).resolve().parents[1] / "src" / "ux_app" / "adapter" / "channel.py"
    source = boot.read_text(encoding="utf-8")
    tree = ast.parse(source)
    found = False
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            found = found or any(a.name.startswith("ux_channel") for a in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            found = found or node.module.startswith("ux_channel")
    # The file must contain the import (lazy, inside a function).
    assert "ux_channel" in source
