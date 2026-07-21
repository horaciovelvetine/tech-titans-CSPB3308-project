"""Flask extension singletons.

Kept in a dedicated module so that models and the app factory can both import
``db`` without creating a circular import.
"""

from __future__ import annotations

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

__all__ = ["db"]
