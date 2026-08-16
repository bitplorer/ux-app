from __future__ import annotations

from pathlib import Path

from ux_app.cli.main import main


def test_add_ui_without_uxdom_writes_pointer(tmp_path: Path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    dest = tmp_path / "app" / "components" / "ui"
    assert main(["add", "ui", "Slider", "--dest", str(dest)]) == 0
    written = list(dest.iterdir())
    assert written
    text = written[0].read_text(encoding="utf-8")
    assert "Slider" in text
    assert "ux-dom" in text
