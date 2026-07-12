# Project Milestone 5: SQL Design

Team 5: Brick Oracle. Backend **SQLite** DB accessed through **SQLAlchemy** via a Flask service layer at [backend/brick-oracle-api/](backend/brick-oracle-api/).

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
- `users`
- `collections`
- `collection_parts`
- `storage_bins`
- `bin_parts`

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

**Query note:** When resolving a set's parts for Brick Diff, always select the inventory with the highest `version` for a given `set_num`. Multiple inventory records can exist per set; using an outdated version will produce incorrect diff results.

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
| img_url | Image URL for the part in this color | Nullable |

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
| img_url    | Image URL for the minifig      | Nullable    |

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
| img_url    | Image URL for the set      | Nullable                |

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
| part_material | Material the part is made of (e.g. Plastic, Rubber) | Nullable |

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

| Field Name | Description                               | Constraints |
| ---------- | ----------------------------------------- | ----------- |
| id         | Unique color identifier                   | Primary key |
| name       | Color display name                        | NOT NULL    |
| rgb        | Hex RGB color value                       | NOT NULL    |
| is_trans   | Whether the color is transparent          | NOT NULL    |
| num_parts  | Number of distinct parts using this color | Nullable    |
| num_sets   | Number of sets that include this color    | Nullable    |
| y1         | First year the color appeared             | Nullable    |
| y2         | Last year the color appeared              | Nullable    |

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
| design_id  | Alternate design identifier  | Nullable                     |

### Relationships

- Many-to-one with `parts`
- Many-to-one with `colors`

---

## 13) Table: users

### Table Description

Stores registered user accounts. Required by User Login, Collection Viewer, Brick Diff, and Collection Storage.

### Fields

| Field Name    | Description                | Constraints      |
| ------------- | -------------------------- | ---------------- |
| id            | Unique user identifier     | Primary key      |
| username      | User's display name        | NOT NULL, UNIQUE |
| email         | User's email address       | NOT NULL, UNIQUE |
| password_hash | Hashed password            | NOT NULL         |
| created_at    | Account creation timestamp | NOT NULL         |

### Relationships

- One-to-many with `collections`
- One-to-many with `storage_bins`

---

## 14) Table: collections

### Table Description

Stores a user's named LEGO collections. A user may have multiple collections. Required by Upload Collection, Collection Viewer, and Brick Diff.

### Fields

| Field Name | Description                   | Constraints                      |
| ---------- | ----------------------------- | -------------------------------- |
| id         | Unique collection identifier  | Primary key                      |
| user_id    | User who owns this collection | Foreign key → users.id, NOT NULL |
| name       | Collection display name       | NOT NULL                         |
| created_at | Collection creation timestamp | NOT NULL                         |

### Relationships

- Many-to-one with `users`
- One-to-many with `collection_parts`

---

## 15) Table: collection_parts

### Table Description

Junction table mapping parts and colors to a user's collection with owned quantity. This table is the user-owned counterpart to `inventory_parts` and is the left-hand side of every Brick Diff calculation. Required by Upload Collection, Collection Viewer, and Brick Diff.

### Fields

| Field Name    | Description                     | Constraints                            |
| ------------- | ------------------------------- | -------------------------------------- |
| id            | Unique record identifier        | Primary key                            |
| collection_id | Collection this part belongs to | Foreign key → collections.id, NOT NULL |
| part_num      | Part identifier                 | Foreign key → parts.part_num, NOT NULL |
| color_id      | Color of the owned part         | Foreign key → colors.id, NOT NULL      |
| quantity      | Number of this part owned       | NOT NULL                               |

### Relationships

- Composite unique constraint on (`collection_id`, `part_num`, `color_id`)
- Many-to-one with `collections`
- Many-to-one with `parts`
- Many-to-one with `colors`

---

## 16) Table: storage_bins

### Table Description

Stores user-defined physical storage bins for organizing LEGO parts. Each bin is user-specific.

### Fields

| Field Name | Description                                | Constraints                      |
| ---------- | ------------------------------------------ | -------------------------------- |
| id         | Unique bin identifier                      | Primary key                      |
| user_id    | User who owns this bin                     | Foreign key → users.id, NOT NULL |
| name       | Bin display name (e.g. "Red Parts Drawer") | NOT NULL                         |

### Relationships

- Many-to-one with `users`
- One-to-many with `bin_parts`

---

## 17) Table: bin_parts

### Table Description

Junction table mapping parts to a storage bin with quantity. A part (by part_num + color_id) can only exist in one bin per user, enforced by a unique constraint.

### Fields

| Field Name | Description                    | Constraints                             |
| ---------- | ------------------------------ | --------------------------------------- |
| id         | Unique record identifier       | Primary key                             |
| bin_id     | Bin this part is stored in     | Foreign key → storage_bins.id, NOT NULL |
| part_num   | Part identifier                | Foreign key → parts.part_num, NOT NULL  |
| color_id   | Color of the stored part       | Foreign key → colors.id, NOT NULL       |
| quantity   | Number of this part in the bin | NOT NULL                                |

### Relationships

- Composite unique constraint on (`part_num`, `color_id`, `bin_id`)
- Many-to-one with `storage_bins`
- Many-to-one with `parts`
- Many-to-one with `colors`

**Constraint note:** To enforce that a brick cannot exist in two bins for the same user, validate on write that the (`part_num`, `color_id`) combination does not already exist in another bin owned by the same user.

---

## 18) Brick Diff Query Pattern

### Description

There is no direct relationship between `sets` and `parts` in the schema. To get the parts for a set you have to join through `inventories`. A set can also have multiple inventory records at different versions, so always use `MAX(version)` to get the correct one.

This join path is used by Brick Diff, Set Viewer, and Set Progress Tracker. Write it once as a shared service method.

### Join Path

```
sets -> inventories (MAX version) -> inventory_parts -> parts + colors
```

### Notes

- `BrickDiffDTO` should include both the set quantity and the user's owned quantity per part so the frontend can render the diff without a second API call
