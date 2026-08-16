"""One default Layout, one content region. No shell / Frame / Main."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Layout:
    name: str = "default"
    content: str = "content"
    regions: tuple[str, ...] = ("content", "notices")
    disposed: bool = False

    def dispose(self) -> None:
        self.disposed = True


def default_layout() -> Layout:
    return Layout()
