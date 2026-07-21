"""Default Flask configuration for the Brick Oracle API."""

from __future__ import annotations

import os
from pathlib import Path


def _default_catalog_data_dir() -> str:
    """Locate ``assets/catalog-data`` by walking up from this file.

    Falls back to the repo-root-relative default even if the folder does not
    yet exist so that config loading itself never fails; the seed step is the
    one that reports a missing directory.
    """
    here = Path(__file__).resolve()
    for candidate in [here, *here.parents]:
        target = candidate / "assets" / "catalog-data"
        if target.is_dir():
            return str(target)
    return str(here.parents[3] / "assets" / "catalog-data")


class Config:
    SQLALCHEMY_DATABASE_URI: str | None = os.environ.get("BRICK_ORACLE_DATABASE_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    CATALOG_DATA_DIR: str = os.environ.get(
        "CATALOG_DATA_DIR", _default_catalog_data_dir()
    )

    SKIP_CATALOG_SEED: bool = bool(os.environ.get("BRICK_ORACLE_SKIP_CATALOG_SEED"))


__all__ = ["Config"]
