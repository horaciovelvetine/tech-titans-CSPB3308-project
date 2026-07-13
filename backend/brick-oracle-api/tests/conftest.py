"""Shared pytest fixtures for the Brick Oracle catalog test suite.

The catalog subsystem reads from ``*.csv.zip`` files that ship in
``assets/catalog-data/``. For fast tests we generate a tiny synthetic
version of those zips in a tmp directory (a handful of rows per table)
and point the Flask app at it via the ``CATALOG_DATA_DIR`` config.
"""

from __future__ import annotations

import io
import zipfile
from pathlib import Path
from typing import Iterable

import pytest


_FIXTURE_ROWS: dict[str, tuple[str, list[list[str]]]] = {
    "part_categories.csv": (
        "id,name",
        [
            ["1", "Baseplates"],
            ["2", "Bricks"],
        ],
    ),
    "colors.csv": (
        "id,name,rgb,is_trans,num_parts,num_sets,y1,y2",
        [
            ["-1", "[Unknown]", "0033B2", "False", "17", "2", "2000", "2000"],
            ["0", "Black", "05131D", "False", "100", "50", "1957", "2026"],
            ["1", "Blue", "0055BF", "False", "80", "40", "1960", "2026"],
        ],
    ),
    "themes.csv": (
        "id,name,parent_id",
        [
            ["1", "Technic", ""],
            ["2", "Star Wars", ""],
            ["3", "Sub Technic", "1"],
        ],
    ),
    "parts.csv": (
        "part_num,name,part_cat_id,part_material",
        [
            ["p001", "Brick 2x4", "2", "Plastic"],
            ["p002", "Baseplate 32x32", "1", "Plastic"],
        ],
    ),
    "minifigs.csv": (
        "fig_num,name,num_parts,img_url",
        [
            ["fig-001", "Astronaut", "4", "http://example.com/fig-001.jpg"],
            ["fig-002", "Diver", "3", ""],
        ],
    ),
    "sets.csv": (
        "set_num,name,year,theme_id,num_parts,img_url",
        [
            ["s-1", "Sample Set", "2020", "1", "42", "http://example.com/s-1.jpg"],
            ["s-2", "Another Set", "2021", "2", "100", ""],
        ],
    ),
    "elements.csv": (
        "element_id,part_num,color_id,design_id",
        [
            ["e001", "p001", "0", ""],
            ["e002", "p002", "1", "designX"],
        ],
    ),
    "part_relationships.csv": (
        "rel_type,child_part_num,parent_part_num",
        [
            ["P", "p001", "p002"],
        ],
    ),
    "inventories.csv": (
        "id,version,set_num",
        [
            ["1", "1", "s-1"],
            ["2", "1", "s-2"],
        ],
    ),
    "inventory_parts.csv": (
        "inventory_id,part_num,color_id,quantity,is_spare,img_url",
        [
            ["1", "p001", "0", "4", "False", ""],
            ["1", "p002", "1", "1", "False", ""],
            ["2", "p001", "1", "2", "True", ""],
        ],
    ),
    "inventory_minifigs.csv": (
        "inventory_id,fig_num,quantity",
        [
            ["1", "fig-001", "1"],
            ["2", "fig-002", "2"],
        ],
    ),
    "inventory_sets.csv": (
        "inventory_id,set_num,quantity",
        [
            ["1", "s-2", "1"],
        ],
    ),
}


def _write_zip(
    target_dir: Path, csv_name: str, header: str, rows: Iterable[list[str]]
) -> None:
    buf = io.StringIO()
    buf.write(header + "\n")
    for row in rows:
        buf.write(",".join(row) + "\n")
    csv_bytes = buf.getvalue().encode("utf-8")

    zip_path = target_dir / f"{csv_name}.zip"
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr(csv_name, csv_bytes)


def build_catalog_fixtures(
    target_dir: Path, *, overrides: dict[str, tuple[str, list[list[str]]]] | None = None
) -> Path:
    """Populate ``target_dir`` with catalog zip fixtures.

    ``overrides`` lets a test replace the header/rows for one or more CSVs
    (used e.g. to force a row-count mismatch that verification must catch).
    """
    target_dir.mkdir(parents=True, exist_ok=True)
    merged = dict(_FIXTURE_ROWS)
    if overrides:
        merged.update(overrides)
    for csv_name, (header, rows) in merged.items():
        _write_zip(target_dir, csv_name, header, rows)
    return target_dir


@pytest.fixture
def catalog_data_dir(tmp_path: Path) -> Path:
    return build_catalog_fixtures(tmp_path / "catalog-data")


@pytest.fixture
def app_config(tmp_path: Path, catalog_data_dir: Path):
    db_path = tmp_path / "brick_oracle_test.sqlite3"
    return {
        "SQLALCHEMY_DATABASE_URI": f"sqlite:///{db_path}",
        "CATALOG_DATA_DIR": str(catalog_data_dir),
        "TESTING": True,
    }
