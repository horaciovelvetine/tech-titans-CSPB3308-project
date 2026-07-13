"""Bulk-load Rebrickable CSV data into the SQLite catalog tables.

Loads happen in dependency order (parents before children) so foreign keys
resolve naturally. Rows stream out of the CSV zip and are inserted using
SQLAlchemy Core in batches, which is dramatically faster than per-row ORM
inserts for the 1.5M-row ``inventory_parts`` table.

The loader deliberately does **not** manage transactions; the orchestrator in
:mod:`brick_oracle_api.catalog.seed` wraps the whole seed in one transaction
so that verification failure can roll every table back atomically.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from sqlalchemy.engine import Connection

from ..models.catalog import CATALOG_LOAD_ORDER
from .csv_source import CatalogTableSpec, spec_for

DEFAULT_BATCH_SIZE = 5_000


@dataclass(frozen=True)
class TableLoadResult:
    table_name: str
    csv_row_count: int


def _batched(
    rows: Iterable[dict[str, object]], batch_size: int
) -> Iterable[list[dict[str, object]]]:
    batch: list[dict[str, object]] = []
    for row in rows:
        batch.append(row)
        if len(batch) >= batch_size:
            yield batch
            batch = []
    if batch:
        yield batch


def load_table(
    connection: Connection,
    model: type,
    data_dir: Path,
    batch_size: int = DEFAULT_BATCH_SIZE,
) -> TableLoadResult:
    spec: CatalogTableSpec = spec_for(model.__tablename__)
    table = model.__table__

    csv_row_count = 0
    insert_stmt = table.insert()
    for batch in _batched(spec.iter_rows(data_dir), batch_size):
        connection.execute(insert_stmt, batch)
        csv_row_count += len(batch)

    return TableLoadResult(table_name=spec.table_name, csv_row_count=csv_row_count)


def load_all_tables(
    connection: Connection,
    data_dir: Path,
    batch_size: int = DEFAULT_BATCH_SIZE,
) -> list[TableLoadResult]:
    results: list[TableLoadResult] = []
    for model in CATALOG_LOAD_ORDER:
        results.append(load_table(connection, model, data_dir, batch_size))
    return results


__all__ = [
    "DEFAULT_BATCH_SIZE",
    "TableLoadResult",
    "load_all_tables",
    "load_table",
]
