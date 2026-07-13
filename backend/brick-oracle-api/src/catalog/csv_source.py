"""Streaming CSV readers for the Rebrickable ``*.csv.zip`` files.

The catalog data ships as one zipped CSV per table in
``assets/catalog-data/``.

Each :class:`CatalogTableSpec` describes the CSV filename, the columns to
keep, and the coercion rules for those columns. The seed loader iterates over
:data:`CATALOG_TABLE_SPECS` in dependency order and only reads the column its inserting.
"""

from __future__ import annotations

import csv
import io
import zipfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, Iterator, Mapping


def _int(value: str) -> int | None:
    value = value.strip()
    if value == "":
        return None
    return int(value)


def _required_int(value: str) -> int:
    parsed = _int(value)
    if parsed is None:
        raise ValueError("expected integer, got empty string")
    return parsed


def _str(value: str) -> str | None:
    if value == "":
        return None
    return value


def _required_str(value: str) -> str:
    if value == "":
        raise ValueError("expected non-empty string")
    return value


_BOOL_TRUE = {"true", "t", "1"}
_BOOL_FALSE = {"false", "f", "0"}


def _bool(value: str) -> bool:
    v = value.strip().lower()
    if v in _BOOL_TRUE:
        return True
    if v in _BOOL_FALSE:
        return False
    raise ValueError(f"unrecognised boolean value: {value!r}")


Coercer = Callable[[str], object]


@dataclass(frozen=True)
class CatalogTableSpec:
    """How to read one CSV zip into rows for one catalog table."""

    table_name: str
    zip_filename: str
    csv_filename: str
    columns: tuple[str, ...]
    coercers: Mapping[str, Coercer] = field(default_factory=dict)

    def iter_rows(self, data_dir: Path) -> Iterator[dict[str, object]]:
        zip_path = data_dir / self.zip_filename
        if not zip_path.is_file():
            raise FileNotFoundError(f"catalog data file not found: {zip_path}")
        with zipfile.ZipFile(zip_path) as zf:
            with zf.open(self.csv_filename, "r") as raw:
                text = io.TextIOWrapper(raw, encoding="utf-8", newline="")
                reader = csv.DictReader(text)
                for raw_row in reader:
                    yield self._coerce_row(raw_row)

    def _coerce_row(self, raw_row: Mapping[str, str]) -> dict[str, object]:
        coerced: dict[str, object] = {}
        for column in self.columns:
            raw_value = raw_row.get(column, "")
            coercer = self.coercers.get(column)
            if coercer is None:
                coerced[column] = _str(raw_value)
            else:
                coerced[column] = coercer(raw_value)
        return coerced


CATALOG_TABLE_SPECS: tuple[CatalogTableSpec, ...] = (
    CatalogTableSpec(
        table_name="part_categories",
        zip_filename="part_categories.csv.zip",
        csv_filename="part_categories.csv",
        columns=("id", "name"),
        coercers={"id": _required_int, "name": _required_str},
    ),
    CatalogTableSpec(
        table_name="colors",
        zip_filename="colors.csv.zip",
        csv_filename="colors.csv",
        columns=("id", "name", "rgb", "is_trans", "num_parts", "num_sets", "y1", "y2"),
        coercers={
            "id": _required_int,
            "name": _required_str,
            "rgb": _required_str,
            "is_trans": _bool,
            "num_parts": _int,
            "num_sets": _int,
            "y1": _int,
            "y2": _int,
        },
    ),
    CatalogTableSpec(
        table_name="themes",
        zip_filename="themes.csv.zip",
        csv_filename="themes.csv",
        columns=("id", "name", "parent_id"),
        coercers={"id": _required_int, "name": _required_str, "parent_id": _int},
    ),
    CatalogTableSpec(
        table_name="parts",
        zip_filename="parts.csv.zip",
        csv_filename="parts.csv",
        columns=("part_num", "name", "part_cat_id", "part_material"),
        coercers={
            "part_num": _required_str,
            "name": _required_str,
            "part_cat_id": _required_int,
            "part_material": _str,
        },
    ),
    CatalogTableSpec(
        table_name="minifigs",
        zip_filename="minifigs.csv.zip",
        csv_filename="minifigs.csv",
        columns=("fig_num", "name", "num_parts", "img_url"),
        coercers={
            "fig_num": _required_str,
            "name": _required_str,
            "num_parts": _required_int,
            "img_url": _str,
        },
    ),
    CatalogTableSpec(
        table_name="sets",
        zip_filename="sets.csv.zip",
        csv_filename="sets.csv",
        columns=("set_num", "name", "year", "theme_id", "num_parts", "img_url"),
        coercers={
            "set_num": _required_str,
            "name": _str,
            "year": _int,
            "theme_id": _int,
            "num_parts": _int,
            "img_url": _str,
        },
    ),
    CatalogTableSpec(
        table_name="elements",
        zip_filename="elements.csv.zip",
        csv_filename="elements.csv",
        columns=("element_id", "part_num", "color_id", "design_id"),
        coercers={
            "element_id": _required_str,
            "part_num": _required_str,
            "color_id": _required_int,
            "design_id": _str,
        },
    ),
    CatalogTableSpec(
        table_name="part_relationships",
        zip_filename="part_relationships.csv.zip",
        csv_filename="part_relationships.csv",
        columns=("rel_type", "child_part_num", "parent_part_num"),
        coercers={
            "rel_type": _required_str,
            "child_part_num": _required_str,
            "parent_part_num": _required_str,
        },
    ),
    CatalogTableSpec(
        table_name="inventories",
        zip_filename="inventories.csv.zip",
        csv_filename="inventories.csv",
        columns=("id", "version", "set_num"),
        coercers={
            "id": _required_int,
            "version": _required_int,
            "set_num": _required_str,
        },
    ),
    CatalogTableSpec(
        table_name="inventory_parts",
        zip_filename="inventory_parts.csv.zip",
        csv_filename="inventory_parts.csv",
        columns=(
            "inventory_id",
            "part_num",
            "color_id",
            "quantity",
            "is_spare",
            "img_url",
        ),
        coercers={
            "inventory_id": _required_int,
            "part_num": _required_str,
            "color_id": _required_int,
            "quantity": _required_int,
            "is_spare": _bool,
            "img_url": _str,
        },
    ),
    CatalogTableSpec(
        table_name="inventory_minifigs",
        zip_filename="inventory_minifigs.csv.zip",
        csv_filename="inventory_minifigs.csv",
        columns=("inventory_id", "fig_num", "quantity"),
        coercers={
            "inventory_id": _required_int,
            "fig_num": _required_str,
            "quantity": _required_int,
        },
    ),
    CatalogTableSpec(
        table_name="inventory_sets",
        zip_filename="inventory_sets.csv.zip",
        csv_filename="inventory_sets.csv",
        columns=("inventory_id", "set_num", "quantity"),
        coercers={
            "inventory_id": _required_int,
            "set_num": _required_str,
            "quantity": _required_int,
        },
    ),
)


_SPECS_BY_TABLE = {spec.table_name: spec for spec in CATALOG_TABLE_SPECS}


def spec_for(table_name: str) -> CatalogTableSpec:
    return _SPECS_BY_TABLE[table_name]


__all__ = [
    "CATALOG_TABLE_SPECS",
    "CatalogTableSpec",
    "Coercer",
    "spec_for",
]
