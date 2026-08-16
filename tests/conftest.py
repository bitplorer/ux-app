from __future__ import annotations

import pytest

from ux_app.action import clear_actions
from ux_app.preview import preview


@pytest.fixture(autouse=True)
def _clean_registry():
    clear_actions()
    preview.clear()
    yield
    clear_actions()
    preview.clear()
