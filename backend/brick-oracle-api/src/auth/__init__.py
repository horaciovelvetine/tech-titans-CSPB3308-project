"""Auth subsystem: registration and login against the ``users`` table."""

from __future__ import annotations

from .routes import auth_bp

__all__ = ["auth_bp"]
