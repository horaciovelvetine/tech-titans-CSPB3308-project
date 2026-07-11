# Project Milestone 5: SQL Design

Team 5: Brick Oracle.
Backend **SQLite** DB accessed through **SQLAlchemy** via a Flask service layer at [backend/brick-oracle-api/](backend/brick-oracle-api/).

# Database Tables

- `inventories`
- `inventory_parts`
- `inventory_minifigs`
- `inventory_sets`
- `minifigs`
- `sets`
- `part_categories`
- `parts`
- `colors`
- `themes`
- `part_relationships`
- `elements`

---

## 1) Table: inventories

### Table Description

Stores inventory records for LEGO sets. Each inventory represents a specific version of a set's contents (parts, minifigs, and sub-sets).

### Fields

| Field Name | Description | Constraints |
| --- | --- | --- |
| id | Unique inventory identifier | Primary key |
| version | Inventory version number | NOT NULL |
| set_num | LEGO set number this inventory belongs to | Foreign key → sets.set_num |

### Relationships

- Many-to-one with `sets` (via `set_num`)
- One-to-many with `inventory_parts`
- One-to-many with `inventory_minifigs`
- One-to-many with `inventory_sets`

---

## 2) Table: inventory_parts

### Table Description

Maps parts (and their colors) to a specific inventory, including quantity and whether the part is a spare.

### Fields

| Field Name | Description | Constraints |
| --- | --- | --- |
| inventory_id | Inventory this part belongs to | Foreign key → inventories.id |
| part_num | Part identifier | Foreign key → parts.part_num |
| color_id | Color of the part | Foreign key → colors.id |
| quantity | Number of this part in the inventory | NOT NULL |
| is_spare | Whether this part is a spare | NOT NULL |

### Relationships

- Composite primary key (`inventory_id`, `part_num`, `color_id`, `is_spare`)
- Many-to-one with `inventories`
- Many-to-one with `parts`
- Many-to-one with `colors`

---

## 3) Table: inventory_minifigs

### Table Description

Maps minifigs to a specific inventory with quantity counts.

### Fields

| Field Name | Description | Constraints |
| --- | --- | --- |
| inventory_id | Inventory this minifig belongs to | Foreign key → inventories.id |
| fig_num | Minifig identifier | Foreign key → minifigs.fig_num |
| quantity | Number of this minifig in the inventory | NOT NULL |

### Relationships

- Composite primary key (`inventory_id`, `fig_num`)
- Many-to-one with `inventories`
- Many-to-one with `minifigs`

---

## 4) Table: inventory_sets

### Table Description

Maps sub-sets included within a specific inventory with quantity counts.

### Fields

| Field Name | Description | Constraints |
| --- | --- | --- |
| inventory_id | Inventory this set belongs to | Foreign key → inventories.id |
| set_num | Set identifier | Foreign key → sets.set_num |
| quantity | Number of this set in the inventory | NOT NULL |

### Relationships

- Composite primary key (`inventory_id`, `set_num`)
- Many-to-one with `inventories`
- Many-to-one with `sets`

---

## 5) Table: minifigs

### Table Description

Stores reference data for LEGO minifigures.

### Fields

| Field Name | Description                    | Constraints |
| ---------- | ------------------------------ | ----------- |
| fig_num    | Unique minifig identifier      | Primary key |
| name       | Minifig display name           | NOT NULL    |
| num_parts  | Number of parts in the minifig | NOT NULL    |

### Relationships

- One-to-many with `inventory_minifigs`

---

## 6) Table: sets

### Table Description

Stores reference data for LEGO sets, including name, release year, theme, and part count.

### Fields

| Field Name | Description                | Constraints             |
| ---------- | -------------------------- | ----------------------- |
| set_num    | Unique set identifier      | Primary key             |
| name       | Set display name           |                         |
| year       | Year the set was released  |                         |
| theme_id   | Theme the set belongs to   | Foreign key → themes.id |
| num_parts  | Number of parts in the set |                         |

### Relationships

- Many-to-one with `themes`
- One-to-many with `inventories`
- One-to-many with `inventory_sets`

---

## 7) Table: part_categories

### Table Description

Stores categories used to classify LEGO parts (e.g., Bricks, Plates, Minifig Parts).

### Fields

| Field Name | Description                | Constraints |
| ---------- | -------------------------- | ----------- |
| id         | Unique category identifier | Primary key |
| name       | Category display name      | NOT NULL    |

### Relationships

- One-to-many with `parts`

---

## 8) Table: parts

### Table Description

Stores reference data for individual LEGO parts.

### Fields

| Field Name | Description | Constraints |
| --- | --- | --- |
| part_num | Unique part identifier | Primary key |
| name | Part display name | NOT NULL |
| part_cat_id | Category this part belongs to | Foreign key → part_categories.id |

### Relationships

- Many-to-one with `part_categories`
- One-to-many with `inventory_parts`
- One-to-many with `elements`
- One-to-many with `part_relationships` (as parent and child)

---

## 9) Table: colors

### Table Description

Stores reference data for LEGO colors, including RGB values and transparency.

### Fields

| Field Name | Description                      | Constraints |
| ---------- | -------------------------------- | ----------- |
| id         | Unique color identifier          | Primary key |
| name       | Color display name               | NOT NULL    |
| rgb        | Hex RGB color value              | NOT NULL    |
| is_trans   | Whether the color is transparent | NOT NULL    |

### Relationships

- One-to-many with `inventory_parts`
- One-to-many with `elements`

---

## 10) Table: themes

### Table Description

Stores LEGO set themes in a hierarchical structure (e.g., Star Wars → The Mandalorian).

### Fields

| Field Name | Description | Constraints |
| --- | --- | --- |
| id | Unique theme identifier | Primary key |
| name | Theme display name | NOT NULL |
| parent_id | Parent theme (for sub-themes) | Foreign key → themes.id, nullable |

### Relationships

- Self-referential many-to-one (via `parent_id`)
- One-to-many with `sets`

---

## 11) Table: part_relationships

### Table Description

Defines parent-child relationships between parts (e.g., assemblies, alternates, or print variants).

### Fields

| Field Name | Description | Constraints |
| --- | --- | --- |
| rel_type | Relationship type code | NOT NULL |
| child_part_num | Child part in the relationship | Foreign key → parts.part_num |
| parent_part_num | Parent part in the relationship | Foreign key → parts.part_num |

### Relationships

- Many-to-one with `parts` (as child via `child_part_num`)
- Many-to-one with `parts` (as parent via `parent_part_num`)

---

## 12) Table: elements

### Table Description

Maps LEGO element IDs to a specific part and color combination. An element is a unique physical brick identified by LEGO's element ID system.

### Fields

| Field Name | Description                  | Constraints                  |
| ---------- | ---------------------------- | ---------------------------- |
| element_id | Unique element identifier    | Primary key                  |
| part_num   | Part this element represents | Foreign key → parts.part_num |
| color_id   | Color of this element        | Foreign key → colors.id      |

### Relationships

- Many-to-one with `parts`
- Many-to-one with `colors`

---
