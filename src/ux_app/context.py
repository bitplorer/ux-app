"""Action context. No Channel types leak out."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, TYPE_CHECKING

from ux_app.events import Continuation

if TYPE_CHECKING:
    from ux_app.app import App


@dataclass
class Principal:
    id: str = "anonymous"
    roles: tuple[str, ...] = ()


@dataclass
class ActionContext:
    app: "App"
    action: str
    args: dict[str, Any]
    principal: Principal = field(default_factory=Principal)
    continuations: list[Continuation] = field(default_factory=list)

    def follow_up(
        self,
        event: str,
        action: str,
        args_from: dict[str, str] | None = None,
        **args: Any,
    ) -> Continuation:
        item = Continuation(
            event=event,
            action=action,
            cap="",
            args_from=dict(args_from or {}),
            args=dict(args),
        )
        self.continuations.append(item)
        return item

    def session_get(self, key: str, default: Any = None) -> Any:
        return self.app.session.get(key, default)

    def session_set(self, key: str, value: Any) -> None:
        self.app.session[key] = value

    def store_get(self, key: str, default: Any = None) -> Any:
        return self.app.store.get(key, default)

    def store_set(self, key: str, value: Any) -> None:
        self.app.store[key] = value
