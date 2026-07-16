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

### Table Tests

**Use Case Name:** Get non-spare parts for an inventory

**Description:** Verify that filtering by `is_spare = false` returns only required parts and excludes spares.

**Pre-conditions:** An inventory exists with at least one spare part and at least one non-spare part.

**Test Steps:**
1. Insert one row with `is_spare = true` and one row with `is_spare = false` for the same `inventory_id`.
2. Query:
   ```sql
   SELECT *
   FROM inventory_parts
   WHERE inventory_id = ?
     AND is_spare = false;
   ```
**Expected Result:** Only the non-spare row is returned.

**Actual Result:** One row returned with `is_spare = false`.

**Status:** Pass

**Post-conditions:** None

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

### Table Tests

**Access method:** Get minifigs by `fig_num`

**Use Case Name:** Validate non-null values

**Description:** Query for missing or invalid database items.

**Pre-conditions:** Database running.

**Test Steps:**
1. Left join `inventory_id` to `inventories`.
2. Left join `fig_num` to `minifigs`.
3. Query for null values.

**Expected Result:** Zero rows are returned.
**Status:** Pass
**Post-conditions:** None

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

### Table Tests

**Use Case Name:** Create valid user

**Description:** Verify that a new user can be inserted and retrieved.

**Pre-conditions:** No user with the given email exists.

**Test Steps:**
1. Insert a valid user row.
2. Query by email.

**Expected Result:** User row exists.
**Actual Result:** User returned by query.
**Status:** Pass
**Post-conditions:** User persisted in database.

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

### Table Tests

**Use Case Name:** Create collection record

**Description:** Verify a new collection can be created in the database.

**Pre-conditions:** Database running.

**Test Steps:**
1. Ensure an existing user row is present in the database.
2. Query the `user_id`.
3. Add a name to the collection record.
4. Insert a collection record with `user_id` and collection name.

**Expected Result:** A collection row is generated with a unique `collection_id`.

**Actual Result:** Collection row is generated with a unique `collection_id`.

**Status:** Pass

**Post-conditions:** User persisted.

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

---

## Data Access Methods

### Method: `get_user_by_email()`

**Description:** Get user by email, takes a string parameter `email` and includes the email in the query. Should return a single row or `None`.

**Parameters:**
- `email` (`str | None`) — unique email of a user

**Return values:**
- `User[user_id, username, email, created_at]` record

**Tests:**
- Assert that passing an email of an existing user returns a single row associated with that unique email.
- Assert that passing an email of a non-existing user returns `None`.
- Assert that passing an invalid argument returns `None`.

**Page:** Called on each page in the application for user context and displaying appropriate data.

---

### Method: `get_sets()`

**Description:** Returns a paginated list of sets with optional filters. Used by the Set Browser page.

**Page:** Set_browser.html

**Parameters:**
- `page` (`int`) — page number
- `page_size` (`int`) — number of results per page
- `search` (`str | None`) — keyword filter on set name; `None` returns all

**Return values:**
- `List`

**Tests:**
- **Use Case Name:** Paginated set list
- **Pre-conditions:** At least 13 sets exist in the database.
- **Expected Result:** 12 sets returned.
- **Status:** Pass

---

### Method: `get_brick_diff()`

**Description:** Computes the diff between a set’s required parts and a user’s owned parts. Returns one `BrickDiffDTO` per part in the set, including both required and owned quantities. Used by Set Builder.

**Page:** Set_builderr.html

**Parameters:**
- `set_num` (`str`) — the set to diff against
- `collection_id` (`int`) — the user’s collection to compare

**Return values:**
- `List[BrickDiffDTO]`

**Tests:**
- **Use Case Name:** Diff with partial collection
- **Pre-conditions:** Set has 3 required parts, user owns two of them.
- **Expected Result:** N DTOs returned.
- **Status:** Pass

---

### Method: `get_latest_inventory()`

**Description:** Fetches the latest inventory records given a specific `set_num`. Fetch all inventories ordered by version, then aggregate records that belong to the highest version inventories.

**Parameters:**
- `set_num` (`str | None`) — set that the inventories belong to

**Return values:**
- `List[inventories]`

**Tests:**
- Assert that a queried `set_num` returns inventories with the latest version.
- Assert that fetched inventories are not older than the highest version.
- Assert that given an invalid `set_num`, `None` is returned.

**Page:** Collection page

---

### Method: `get_collection_parts()`

**Description:** Return all of the parts in a user’s collection.

**Page:** `collection_browser.html`

**Parameters:**
- `user_id` (`int`)
- `collection_id` (`int`)

**Return values:**
- `part_num` (`int`)
- `color_name` (`string`)
- `part_quantity` (`int`)

**Tests:**
- Assert that a `collection_id` with the wrong `user_id` returns no rows.
- Assert that a `user_id` with the wrong `collection_id` returns no rows.
- Assert that a correct `user_id` with a correct `collection_id` returns matching parts.

