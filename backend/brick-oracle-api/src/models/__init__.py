"""SQLAlchemy models for the Brick Oracle API."""

from __future__ import annotations

from .catalog import (
    CATALOG_LOAD_ORDER,
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
    Set as LegoSet,
    Theme,
)

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
    "LegoSet",
    "Minifig",
    "Part",
    "PartCategory",
    "PartRelationship",
    "Theme",
]
