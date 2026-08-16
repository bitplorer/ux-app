"""Public error types. No Channel / CEK imports."""

from __future__ import annotations


class AppError(Exception):
    """Base error for the application layer."""


class IsolationError(AppError):
    """A non-adapter module imported Channel or CEK."""


class DoctorError(AppError):
    """Doctor found a failed check."""

    def __init__(self, issues: list[str]):
        self.issues = list(issues)
        super().__init__("doctor failed:\n  - " + "\n  - ".join(self.issues))


class ValidationError(AppError):
    """Action or field validation miss (not a Cap refusal)."""

    def __init__(self, message: str, *, fields: dict[str, str] | None = None):
        self.fields = dict(fields or {})
        super().__init__(message)


class IllegalOp(AppError):
    """Pair is not in S and not on the session stamp, or name is not a token."""


class AuthorityRefusal(AppError):
    """Cap verify failed. Callers must treat this unlike validation."""

    def __init__(self, reason: str):
        self.reason = reason
        super().__init__(reason)


class DispatchError(AppError):
    """Verified, then the handler or policy missed."""
