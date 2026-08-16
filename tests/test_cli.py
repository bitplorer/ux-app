from __future__ import annotations

from pathlib import Path

from ux_app.cli.main import main


def test_doctor_ok():
    assert main(["doctor"]) == 0


def test_doctor_fail_flag_exists():
    # Package is clean; --fail still exits 0.
    assert main(["doctor", "--fail"]) == 0


def test_explain_runs():
    assert main(["explain"]) == 0


def test_create_app_layers_and_respects_force(tmp_path: Path, monkeypatch):
    dest = tmp_path / "shop"
    assert main(["create-app", str(dest), "--yes"]) == 0
    assert (dest / "app.py").is_file()
    original = (dest / "app.py").read_text(encoding="utf-8")
    (dest / "app.py").write_text("keep\n", encoding="utf-8")
    assert main(["create-app", str(dest), "--yes"]) == 0
    assert (dest / "app.py").read_text(encoding="utf-8") == "keep\n"
    assert main(["create-app", str(dest), "--yes", "--force"]) == 0
    assert (dest / "app.py").read_text(encoding="utf-8") != "keep\n"
    assert original.count("\n") >= 1


def test_yes_is_not_force(tmp_path: Path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    (tmp_path / "app.py").write_text("existing\n", encoding="utf-8")
    assert main(["init", "--yes"]) == 0
    assert (tmp_path / "app.py").read_text(encoding="utf-8") == "existing\n"


def test_new_component(tmp_path: Path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    assert main(["new", "component", "banner"]) == 0
    assert (tmp_path / "banner.py").is_file()
    assert "chrome" not in (tmp_path / "banner.py").read_text(encoding="utf-8")


def test_new_action_and_domain(tmp_path: Path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    assert main(["new", "action", "orders.create"]) == 0
    assert main(["new", "domain", "orders"]) == 0
    assert (tmp_path / "orders_create.py").is_file()
    assert (tmp_path / "orders_domain.py").is_file()
