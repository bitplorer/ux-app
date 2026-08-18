"""Adapter boundary.

This package is the only place that may import ux_channel or cek_*.
Submodules lazy-import those cores so a cold ``import ux_app`` stays clean.
The in-process runtime in runtime.py does not import the cores.

``lower`` / ``compose`` speak Channel *wire shape* without importing
ux_channel. They live here so every Host does not reimplement the crossing.
"""

from ux_app.adapter.compose import ComposeConflict, compose
from ux_app.adapter.lower import as_selector, lower_morph

__all__ = [
    "ComposeConflict",
    "as_selector",
    "compose",
    "lower_morph",
]
