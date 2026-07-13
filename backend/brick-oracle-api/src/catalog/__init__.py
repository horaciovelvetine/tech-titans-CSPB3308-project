"""Immutable Rebrickable catalog subsystem.

Public entrypoint is :func:`brick_oracle_api.catalog.seed.ensure_catalog_loaded`,
called from the app factory. Everything else in this package is an
implementation detail of that seed process.
"""

from __future__ import annotations

from .seed import CatalogSeedError, ensure_catalog_loaded

__all__ = ["CatalogSeedError", "ensure_catalog_loaded"]
