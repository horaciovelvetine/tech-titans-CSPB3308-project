"""Orchestrate the one-time catalog seed on Flask app startup.

High level flow (see the plan doc for the sequence diagram):

1. If the ``catalog_metadata`` marker table already has a row, do nothing.
2. Otherwise, inside a single transaction:
   a. Wipe any partial catalog rows left over from an earlier failed run.
   b. Bulk-load every catalog table from the ``*.csv.zip`` files.
   c. Verify per-table CSV row counts match ``SELECT COUNT(*)`` in the DB.
   d. Install the SQLite immutability triggers.
   e. Insert the marker row so subsequent startups are cheap no-ops.

Any failure inside the transaction rolls the whole thing back so the app
never boots with a partially-seeded catalog.
"""

from __future__ import annotations

import json
import logging
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

from flask import Flask
from sqlalchemy import event, select, text
from sqlalchemy.engine import Engine

from ..extensions import db
from ..models.catalog import CATALOG_LOAD_ORDER, CatalogMetadata
from .loader import DEFAULT_BATCH_SIZE, TableLoadResult, load_all_tables
from .triggers import install_immutability_triggers
from .verify import CatalogVerificationError, verify_row_counts

logger = logging.getLogger(__name__)


class CatalogSeedError(RuntimeError):
    """Raised when the catalog cannot be seeded."""


@dataclass(frozen=True)
class SeedSummary:
    seeded: bool
    row_counts: dict[str, int]


_SQLITE_FK_LISTENER_INSTALLED = False


def _install_sqlite_fk_pragma(engine: Engine) -> None:
    """Ensure ``PRAGMA foreign_keys=ON`` on every SQLite connection.

    Flask-SQLAlchemy pools connections; SQLite defaults to FK enforcement
    off, so we listen for new connections and flip it on once.
    """
    global _SQLITE_FK_LISTENER_INSTALLED
    if _SQLITE_FK_LISTENER_INSTALLED:
        return
    if engine.dialect.name != "sqlite":
        return

    @event.listens_for(engine, "connect")
    def _on_connect(dbapi_connection, _):
        cursor = dbapi_connection.cursor()
        try:
            cursor.execute("PRAGMA foreign_keys=ON")
        finally:
            cursor.close()

    _SQLITE_FK_LISTENER_INSTALLED = True


def _catalog_already_seeded() -> bool:
    stmt = select(CatalogMetadata).limit(1)
    return db.session.execute(stmt).scalar_one_or_none() is not None


def _resolve_data_dir(app: Flask) -> Path:
    raw = app.config.get("CATALOG_DATA_DIR")
    if not raw:
        raise CatalogSeedError(
            "CATALOG_DATA_DIR is not configured; cannot locate catalog CSVs"
        )
    path = Path(raw)
    if not path.is_dir():
        raise CatalogSeedError(
            f"CATALOG_DATA_DIR does not exist or is not a directory: {path}"
        )
    return path


def _wipe_catalog_tables(connection) -> None:
    for model in reversed(CATALOG_LOAD_ORDER):
        connection.execute(model.__table__.delete())


_FAST_SEED_PRAGMAS = (
    "PRAGMA synchronous=OFF",
    "PRAGMA journal_mode=MEMORY",
    "PRAGMA foreign_keys=OFF",
)

_RESTORE_PRAGMAS = (
    "PRAGMA foreign_keys=ON",
    "PRAGMA synchronous=NORMAL",
    "PRAGMA journal_mode=DELETE",
)


def _apply_pragmas(engine: Engine, pragmas: tuple[str, ...]) -> None:
    """Apply pragma statements outside of any transaction.

    ``synchronous`` and ``journal_mode`` cannot be changed inside a running
    transaction, so we open a dedicated AUTOCOMMIT connection just for them.
    """
    if engine.dialect.name != "sqlite":
        return
    with engine.connect().execution_options(isolation_level="AUTOCOMMIT") as connection:
        for stmt in pragmas:
            connection.execute(text(stmt))


def ensure_catalog_loaded(
    app: Flask, *, batch_size: int = DEFAULT_BATCH_SIZE
) -> SeedSummary:
    """Seed the catalog if it hasn't been seeded already.

    Safe to call on every startup. Returns a :class:`SeedSummary` describing
    whether work was done and, if so, the per-table row counts.
    """
    engine = db.engine
    _install_sqlite_fk_pragma(engine)

    if _catalog_already_seeded():
        logger.info("catalog already seeded, skipping load")
        return SeedSummary(seeded=False, row_counts={})

    data_dir = _resolve_data_dir(app)
    logger.info("seeding catalog from %s", data_dir)

    _apply_pragmas(engine, _FAST_SEED_PRAGMAS)

    row_counts: dict[str, int] = {}
    try:
        with engine.begin() as connection:
            _wipe_catalog_tables(connection)

            results: list[TableLoadResult] = load_all_tables(
                connection, data_dir, batch_size=batch_size
            )
            verify_row_counts(connection, results)

            install_immutability_triggers(connection)

            row_counts = {r.table_name: r.csv_row_count for r in results}
            connection.execute(
                CatalogMetadata.__table__.insert().values(
                    seeded_at=datetime.now(timezone.utc),
                    source_row_counts=json.dumps(row_counts, sort_keys=True),
                )
            )
    except CatalogVerificationError as exc:
        logger.error("catalog verification failed: %s", exc)
        raise CatalogSeedError(str(exc)) from exc
    except FileNotFoundError as exc:
        raise CatalogSeedError(str(exc)) from exc
    finally:
        _apply_pragmas(engine, _RESTORE_PRAGMAS)

    logger.info("catalog seed complete: %s", row_counts)
    return SeedSummary(seeded=True, row_counts=row_counts)


__all__ = [
    "CatalogSeedError",
    "SeedSummary",
    "ensure_catalog_loaded",
]
