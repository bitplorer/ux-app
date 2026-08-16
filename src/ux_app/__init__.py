"""Host-authored application layer on ux-dom + ux-channel.

Cold ``import ux_app`` does not import Channel, CEK, or wire codecs.
"""

from ux_app._version import __version__, __version_info__
from ux_app.action import action
from ux_app.app import App
from ux_app.component import Component
from ux_app.events import follow_up
from ux_app.html import Badge
from ux_app.ops import Op, go, notify, update
from ux_app.preview import preview
from ux_app.state import Client, Sealed, Store, Transient

__all__ = [
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
    "Store",
    "Transient",
    "Sealed",
    "Badge",
    "__version__",
]
