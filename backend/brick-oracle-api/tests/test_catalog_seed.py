"""Tests for the immutable catalog seeding pipeline."""

from __future__ import annotations

from pathlib import Path

import pytest
from sqlalchemy import func, select, text
from sqlalchemy.exc import IntegrityError, OperationalError

from src import create_app
from src.catalog.seed import CatalogSeedError
from src.extensions import db
from src.models.catalog import (
    CATALOG_MODELS,
    CatalogMetadata,
    Part,
    Set,
)


def _table_row_counts(app) -> dict[str, int]:
    with app.app_context():
        return {
            model.__tablename__: db.session.execute(
                select(func.count()).select_from(model.__table__)
            ).scalar_one()
            for model in CATALOG_MODELS
        }


def test_catalog_seeds_all_tables(app_config):
    app = create_app(app_config)

    with app.app_context():
        marker = db.session.execute(select(CatalogMetadata)).scalar_one_or_none()
        assert marker is not None, "catalog_metadata marker must exist after seed"

    counts = _table_row_counts(app)
    assert counts["part_categories"] == 2
    assert counts["colors"] == 3
    assert counts["themes"] == 3
    assert counts["parts"] == 2
    assert counts["minifigs"] == 2
    assert counts["sets"] == 2
    assert counts["elements"] == 2
    assert counts["part_relationships"] == 1
    assert counts["inventories"] == 2
    assert counts["inventory_parts"] == 3
    assert counts["inventory_minifigs"] == 2
    assert counts["inventory_sets"] == 1

    with app.app_context():
        part = db.session.get(Part, "p001")
        assert part is not None
        assert part.name == "Brick 2x4"
        assert part.part_material == "Plastic"

        lego_set = db.session.get(Set, "s-1")
        assert lego_set is not None
        assert lego_set.img_url == "http://example.com/s-1.jpg"


def test_catalog_seed_is_idempotent(app_config):
    app_first = create_app(app_config)
    counts_first = _table_row_counts(app_first)

    app_second = create_app(app_config)
    counts_second = _table_row_counts(app_second)

    assert counts_first == counts_second

    with app_second.app_context():
        markers = db.session.execute(select(CatalogMetadata)).scalars().all()
        assert len(markers) == 1, "seeding must never write a second marker row"


def test_row_count_mismatch_aborts_seed(app_config, monkeypatch: pytest.MonkeyPatch):
    """Simulate a lost-row scenario by inflating the reported CSV count.

    The loader normally reports the exact number of rows it inserted, so a
    natural mismatch cannot happen without an underlying insert failure.
    We patch the loader to over-report by 5, which is enough to make
    verification fail and abort the seed transaction.
    """
    from src.catalog import loader as loader_mod
    from src.catalog import seed as seed_mod

    original_load_all_tables = loader_mod.load_all_tables

    def inflated_load_all_tables(connection, data_dir, batch_size=None):
        kwargs = {} if batch_size is None else {"batch_size": batch_size}
        results = original_load_all_tables(connection, data_dir, **kwargs)
        inflated = []
        for r in results:
            if r.table_name == "colors":
                inflated.append(
                    loader_mod.TableLoadResult(
                        table_name=r.table_name,
                        csv_row_count=r.csv_row_count + 5,
                    )
                )
            else:
                inflated.append(r)
        return inflated

    monkeypatch.setattr(seed_mod, "load_all_tables", inflated_load_all_tables)

    with pytest.raises(CatalogSeedError):
        create_app(app_config)

    app_config_with_seed_skipped = dict(app_config)
    app_config_with_seed_skipped["SKIP_CATALOG_SEED"] = True
    app = create_app(app_config_with_seed_skipped)
    with app.app_context():
        assert (
            db.session.execute(select(CatalogMetadata)).scalar_one_or_none() is None
        ), "marker row must not be written when verification aborts the seed"


def test_immutability_triggers_block_update_and_delete(app_config):
    app = create_app(app_config)

    with app.app_context():
        with pytest.raises((IntegrityError, OperationalError)):
            db.session.execute(
                text("UPDATE parts SET name='hacked' WHERE part_num='p001'")
            )
            db.session.commit()
        db.session.rollback()

        with pytest.raises((IntegrityError, OperationalError)):
            db.session.execute(text("DELETE FROM parts WHERE part_num='p001'"))
            db.session.commit()
        db.session.rollback()

        part = db.session.get(Part, "p001")
        assert part is not None
        assert part.name == "Brick 2x4"


def test_immutability_triggers_survive_restart(app_config):
    create_app(app_config)

    app = create_app(app_config)
    with app.app_context():
        with pytest.raises((IntegrityError, OperationalError)):
            db.session.execute(text("DELETE FROM colors"))
            db.session.commit()
        db.session.rollback()
