"""SQLite immutability triggers for the catalog tables.

Once seeding succeeds we install a ``BEFORE UPDATE`` and ``BEFORE DELETE``
trigger on every one of the 12 catalog tables that raises ``RAISE(ABORT, ...)``
whenever the app (or a curious DBA) tries to mutate a row. The triggers live
in the SQLite file itself, so they stay in force across every subsequent
startup even though the seed step is skipped once the marker row exists.

The ``catalog_metadata`` marker table is intentionally *not* covered by these
triggers -- it needs to be writable on the initial seed run.
"""

from __future__ import annotations

from sqlalchemy import text
from sqlalchemy.engine import Connection

from ..models.catalog import CATALOG_MODELS


def _trigger_sql(table_name: str) -> tuple[str, str]:
    update_trigger = f"""
        CREATE TRIGGER IF NOT EXISTS trg_{table_name}_no_update
        BEFORE UPDATE ON {table_name}
        BEGIN
            SELECT RAISE(ABORT, '{table_name} is immutable catalog data');
        END
    """
    delete_trigger = f"""
        CREATE TRIGGER IF NOT EXISTS trg_{table_name}_no_delete
        BEFORE DELETE ON {table_name}
        BEGIN
            SELECT RAISE(ABORT, '{table_name} is immutable catalog data');
        END
    """
    return update_trigger, delete_trigger


def install_immutability_triggers(connection: Connection) -> None:
    for model in CATALOG_MODELS:
        update_sql, delete_sql = _trigger_sql(model.__tablename__)
        connection.execute(text(update_sql))
        connection.execute(text(delete_sql))


def drop_immutability_triggers(connection: Connection) -> None:
    """Used only by tests that need to tear down the catalog explicitly."""
    for model in CATALOG_MODELS:
        table_name = model.__tablename__
        connection.execute(text(f"DROP TRIGGER IF EXISTS trg_{table_name}_no_update"))
        connection.execute(text(f"DROP TRIGGER IF EXISTS trg_{table_name}_no_delete"))


__all__ = [
    "drop_immutability_triggers",
    "install_immutability_triggers",
]
