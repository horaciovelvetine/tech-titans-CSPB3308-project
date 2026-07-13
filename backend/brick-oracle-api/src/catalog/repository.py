"""Read-only query helpers over the immutable catalog.

Only ``get_*`` and ``list_*`` methods live here; no create/update/delete
helpers are exposed to enforce the app-layer immutability convention
alongside the DB-level triggers installed by
:mod:`brick_oracle_api.catalog.triggers`.

All queries run against the Flask-SQLAlchemy session bound to the current
app context.
"""

from __future__ import annotations

from typing import Sequence

from sqlalchemy import func, select

from ..extensions import db
from ..models.catalog import (
    CATALOG_MODELS,
    CatalogMetadata,
    Color,
    Element,
    Inventory,
    InventoryMinifig,
    InventoryPart,
    InventorySet,
    Minifig,
    Part,
    PartCategory,
    PartRelationship,
    Set,
    Theme,
)


def table_row_counts() -> dict[str, int]:
    counts = {
        model.__tablename__: db.session.execute(
            select(func.count()).select_from(model.__table__)
        ).scalar_one()
        for model in CATALOG_MODELS
    }
    counts[CatalogMetadata.__tablename__] = db.session.execute(
        select(func.count()).select_from(CatalogMetadata.__table__)
    ).scalar_one()
    return counts


def get_set(set_num: str) -> Set | None:
    return db.session.get(Set, set_num)


def list_sets(limit: int = 50, offset: int = 0) -> Sequence[Set]:
    stmt = select(Set).order_by(Set.set_num).limit(limit).offset(offset)
    return db.session.execute(stmt).scalars().all()


def get_part(part_num: str) -> Part | None:
    return db.session.get(Part, part_num)


def list_parts_by_category(part_cat_id: int) -> Sequence[Part]:
    stmt = select(Part).where(Part.part_cat_id == part_cat_id).order_by(Part.part_num)
    return db.session.execute(stmt).scalars().all()


def get_color(color_id: int) -> Color | None:
    return db.session.get(Color, color_id)


def list_colors() -> Sequence[Color]:
    return db.session.execute(select(Color).order_by(Color.id)).scalars().all()


def get_theme(theme_id: int) -> Theme | None:
    return db.session.get(Theme, theme_id)


def list_root_themes() -> Sequence[Theme]:
    stmt = select(Theme).where(Theme.parent_id.is_(None)).order_by(Theme.name)
    return db.session.execute(stmt).scalars().all()


def get_minifig(fig_num: str) -> Minifig | None:
    return db.session.get(Minifig, fig_num)


def get_part_category(category_id: int) -> PartCategory | None:
    return db.session.get(PartCategory, category_id)


def list_part_categories() -> Sequence[PartCategory]:
    return (
        db.session.execute(select(PartCategory).order_by(PartCategory.id))
        .scalars()
        .all()
    )


def get_inventory(inventory_id: int) -> Inventory | None:
    return db.session.get(Inventory, inventory_id)


def list_inventories_for_set(set_num: str) -> Sequence[Inventory]:
    stmt = (
        select(Inventory)
        .where(Inventory.set_num == set_num)
        .order_by(Inventory.version)
    )
    return db.session.execute(stmt).scalars().all()


def list_inventory_parts(inventory_id: int) -> Sequence[InventoryPart]:
    stmt = select(InventoryPart).where(InventoryPart.inventory_id == inventory_id)
    return db.session.execute(stmt).scalars().all()


def list_inventory_minifigs(inventory_id: int) -> Sequence[InventoryMinifig]:
    stmt = select(InventoryMinifig).where(InventoryMinifig.inventory_id == inventory_id)
    return db.session.execute(stmt).scalars().all()


def list_inventory_sets(inventory_id: int) -> Sequence[InventorySet]:
    stmt = select(InventorySet).where(InventorySet.inventory_id == inventory_id)
    return db.session.execute(stmt).scalars().all()


def list_elements_for_part(part_num: str) -> Sequence[Element]:
    stmt = select(Element).where(Element.part_num == part_num)
    return db.session.execute(stmt).scalars().all()


def list_part_relationships_for_part(part_num: str) -> Sequence[PartRelationship]:
    stmt = select(PartRelationship).where(
        (PartRelationship.child_part_num == part_num)
        | (PartRelationship.parent_part_num == part_num)
    )
    return db.session.execute(stmt).scalars().all()


__all__ = [
    "get_color",
    "get_inventory",
    "get_minifig",
    "get_part",
    "get_part_category",
    "get_set",
    "get_theme",
    "list_colors",
    "list_elements_for_part",
    "list_inventories_for_set",
    "list_inventory_minifigs",
    "list_inventory_parts",
    "list_inventory_sets",
    "list_part_categories",
    "list_part_relationships_for_part",
    "list_parts_by_category",
    "list_root_themes",
    "list_sets",
    "table_row_counts",
]
