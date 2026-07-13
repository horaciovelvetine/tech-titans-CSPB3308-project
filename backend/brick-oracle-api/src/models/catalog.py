"""SQLAlchemy models for the Rebrickable catalog tables.

Column definitions mirror the schema documented in :doc:`SQL_TESTING.md`

The 12 catalog models are treated as an **immutable base layer**: no create,
update, or delete helpers are exposed anywhere in the application, and
SQLite triggers installed by the seed process block ``UPDATE``/``DELETE`` at
the database level as an additional safeguard.
"""

from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    Integer,
    PrimaryKeyConstraint,
    String,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..extensions import db


class PartCategory(db.Model):
    __tablename__ = "part_categories"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=False)
    name: Mapped[str] = mapped_column(String(200), nullable=False)

    parts: Mapped[List["Part"]] = relationship(back_populates="category")


class Color(db.Model):
    __tablename__ = "colors"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=False)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    rgb: Mapped[str] = mapped_column(String(6), nullable=False)
    is_trans: Mapped[bool] = mapped_column(Boolean, nullable=False)
    num_parts: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    num_sets: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    y1: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    y2: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    inventory_parts: Mapped[List["InventoryPart"]] = relationship(
        back_populates="color"
    )
    elements: Mapped[List["Element"]] = relationship(back_populates="color")


class Theme(db.Model):
    __tablename__ = "themes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=False)
    name: Mapped[str] = mapped_column(String(40), nullable=False)
    parent_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("themes.id"), nullable=True
    )

    parent: Mapped[Optional["Theme"]] = relationship(
        remote_side="Theme.id", back_populates="children"
    )
    children: Mapped[List["Theme"]] = relationship(back_populates="parent")
    sets: Mapped[List["Set"]] = relationship(back_populates="theme")


class Part(db.Model):
    __tablename__ = "parts"

    part_num: Mapped[str] = mapped_column(String(20), primary_key=True)
    name: Mapped[str] = mapped_column(String(250), nullable=False)
    part_cat_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("part_categories.id"), nullable=False
    )
    part_material: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)

    category: Mapped["PartCategory"] = relationship(back_populates="parts")
    inventory_parts: Mapped[List["InventoryPart"]] = relationship(back_populates="part")
    elements: Mapped[List["Element"]] = relationship(back_populates="part")
    child_relationships: Mapped[List["PartRelationship"]] = relationship(
        foreign_keys="PartRelationship.child_part_num",
        back_populates="child_part",
    )
    parent_relationships: Mapped[List["PartRelationship"]] = relationship(
        foreign_keys="PartRelationship.parent_part_num",
        back_populates="parent_part",
    )


class Minifig(db.Model):
    __tablename__ = "minifigs"

    fig_num: Mapped[str] = mapped_column(String(20), primary_key=True)
    name: Mapped[str] = mapped_column(String(256), nullable=False)
    num_parts: Mapped[int] = mapped_column(Integer, nullable=False)
    img_url: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    inventory_minifigs: Mapped[List["InventoryMinifig"]] = relationship(
        back_populates="minifig"
    )


class Set(db.Model):
    __tablename__ = "sets"

    set_num: Mapped[str] = mapped_column(String(20), primary_key=True)
    name: Mapped[Optional[str]] = mapped_column(String(256), nullable=True)
    year: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    theme_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("themes.id"), nullable=True
    )
    num_parts: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    img_url: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    theme: Mapped[Optional["Theme"]] = relationship(back_populates="sets")
    inventories: Mapped[List["Inventory"]] = relationship(back_populates="set")
    inventory_sets: Mapped[List["InventorySet"]] = relationship(back_populates="set")


class Element(db.Model):
    __tablename__ = "elements"

    element_id: Mapped[str] = mapped_column(String(10), primary_key=True)
    part_num: Mapped[str] = mapped_column(
        String(20), ForeignKey("parts.part_num"), nullable=False
    )
    color_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("colors.id"), nullable=False
    )
    design_id: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)

    part: Mapped["Part"] = relationship(back_populates="elements")
    color: Mapped["Color"] = relationship(back_populates="elements")


class PartRelationship(db.Model):
    __tablename__ = "part_relationships"
    __table_args__ = (
        PrimaryKeyConstraint(
            "rel_type",
            "child_part_num",
            "parent_part_num",
            name="pk_part_relationships",
        ),
    )

    rel_type: Mapped[str] = mapped_column(String(1), nullable=False)
    child_part_num: Mapped[str] = mapped_column(
        String(20), ForeignKey("parts.part_num"), nullable=False
    )
    parent_part_num: Mapped[str] = mapped_column(
        String(20), ForeignKey("parts.part_num"), nullable=False
    )

    child_part: Mapped["Part"] = relationship(
        foreign_keys=[child_part_num], back_populates="child_relationships"
    )
    parent_part: Mapped["Part"] = relationship(
        foreign_keys=[parent_part_num], back_populates="parent_relationships"
    )


class Inventory(db.Model):
    __tablename__ = "inventories"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=False)
    version: Mapped[int] = mapped_column(Integer, nullable=False)
    set_num: Mapped[str] = mapped_column(
        String(20), ForeignKey("sets.set_num"), nullable=False
    )

    set: Mapped["Set"] = relationship(back_populates="inventories")
    inventory_parts: Mapped[List["InventoryPart"]] = relationship(
        back_populates="inventory"
    )
    inventory_minifigs: Mapped[List["InventoryMinifig"]] = relationship(
        back_populates="inventory"
    )
    inventory_sets: Mapped[List["InventorySet"]] = relationship(
        back_populates="inventory"
    )


class InventoryPart(db.Model):
    __tablename__ = "inventory_parts"
    __table_args__ = (
        PrimaryKeyConstraint(
            "inventory_id",
            "part_num",
            "color_id",
            "is_spare",
            name="pk_inventory_parts",
        ),
    )

    inventory_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("inventories.id"), nullable=False
    )
    part_num: Mapped[str] = mapped_column(
        String(20), ForeignKey("parts.part_num"), nullable=False
    )
    color_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("colors.id"), nullable=False
    )
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    is_spare: Mapped[bool] = mapped_column(Boolean, nullable=False)
    img_url: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    inventory: Mapped["Inventory"] = relationship(back_populates="inventory_parts")
    part: Mapped["Part"] = relationship(back_populates="inventory_parts")
    color: Mapped["Color"] = relationship(back_populates="inventory_parts")


class InventoryMinifig(db.Model):
    __tablename__ = "inventory_minifigs"
    __table_args__ = (
        PrimaryKeyConstraint("inventory_id", "fig_num", name="pk_inventory_minifigs"),
    )

    inventory_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("inventories.id"), nullable=False
    )
    fig_num: Mapped[str] = mapped_column(
        String(20), ForeignKey("minifigs.fig_num"), nullable=False
    )
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)

    inventory: Mapped["Inventory"] = relationship(back_populates="inventory_minifigs")
    minifig: Mapped["Minifig"] = relationship(back_populates="inventory_minifigs")


class InventorySet(db.Model):
    __tablename__ = "inventory_sets"
    __table_args__ = (
        PrimaryKeyConstraint("inventory_id", "set_num", name="pk_inventory_sets"),
    )

    inventory_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("inventories.id"), nullable=False
    )
    set_num: Mapped[str] = mapped_column(
        String(20), ForeignKey("sets.set_num"), nullable=False
    )
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)

    inventory: Mapped["Inventory"] = relationship(back_populates="inventory_sets")
    set: Mapped["Set"] = relationship(back_populates="inventory_sets")


class CatalogMetadata(db.Model):
    """Single-row marker table used to detect an already-seeded catalog.

    ``source_row_counts`` records per-table CSV data-row counts from the seed
    run, primarily for post-hoc verification/debugging.
    """

    __tablename__ = "catalog_metadata"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    seeded_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    source_row_counts: Mapped[str] = mapped_column(Text, nullable=False)


CATALOG_LOAD_ORDER: tuple[type[db.Model], ...] = (
    PartCategory,
    Color,
    Theme,
    Part,
    Minifig,
    Set,
    Element,
    PartRelationship,
    Inventory,
    InventoryPart,
    InventoryMinifig,
    InventorySet,
)

CATALOG_MODELS: tuple[type[db.Model], ...] = CATALOG_LOAD_ORDER


__all__ = [
    "CATALOG_LOAD_ORDER",
    "CATALOG_MODELS",
    "CatalogMetadata",
    "Color",
    "Element",
    "Inventory",
    "InventoryMinifig",
    "InventoryPart",
    "InventorySet",
    "Minifig",
    "Part",
    "PartCategory",
    "PartRelationship",
    "Set",
    "Theme",
]
