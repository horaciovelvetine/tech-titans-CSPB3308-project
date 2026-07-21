"""Post-load verification for the seeded catalog.

For every table, compare the number of data rows the loader observed in the
CSV against the number of rows actually persisted in SQLite. Any mismatch is
treated as a hard failure so the seed transaction can be rolled back before
the app starts serving requests.
"""

from __future__ import annotations

from dataclasses import dataclass

from sqlalchemy import func, select
from sqlalchemy.engine import Connection

from ..models.catalog import CATALOG_LOAD_ORDER
from .loader import TableLoadResult


@dataclass(frozen=True)
class TableCountMismatch:
    table_name: str
    csv_count: int
    db_count: int


class CatalogVerificationError(RuntimeError):
    def __init__(self, mismatches: list[TableCountMismatch]) -> None:
        self.mismatches = mismatches
        details = ", ".join(
            f"{m.table_name}: csv={m.csv_count} db={m.db_count}" for m in mismatches
        )
        super().__init__(f"catalog row-count verification failed: {details}")


def _db_row_count(connection: Connection, model: type) -> int:
    stmt = select(func.count()).select_from(model.__table__)
    return int(connection.execute(stmt).scalar_one())


def verify_row_counts(
    connection: Connection, load_results: list[TableLoadResult]
) -> None:
    results_by_table = {r.table_name: r for r in load_results}
    mismatches: list[TableCountMismatch] = []
    for model in CATALOG_LOAD_ORDER:
        table_name = model.__tablename__
        expected = results_by_table[table_name].csv_row_count
        actual = _db_row_count(connection, model)
        if expected != actual:
            mismatches.append(
                TableCountMismatch(
                    table_name=table_name,
                    csv_count=expected,
                    db_count=actual,
                )
            )
    if mismatches:
        raise CatalogVerificationError(mismatches)


__all__ = [
    "CatalogVerificationError",
    "TableCountMismatch",
    "verify_row_counts",
]
