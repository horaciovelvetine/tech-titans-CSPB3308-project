# Brick Oracle Final Report

## Project Title
Brick Oracle — LEGO Collection Management and Set Completion Tracker

## Team Members
- Theodore Matthews
- James Tillman
- Owen Ahlers
- Woobin Huh

## Required Links

- Project tracker: [GitHub Issues](https://github.com/horaciovelvetine/tech-titans-CSPB3308-project/issues)
- Repository: [GitHub Repo](https://github.com/horaciovelvetine/tech-titans-CSPB3308-project)
- Demo video: [Demo Video](https://github.com/horaciovelvetine/tech-titans-CSPB3308-project/blob/master/brick_oracle_demo.mp4)
- Public deployment: Not deployed. See setup instructions below.

## Local Setup

### Backend
```bash
cd backend/brick-oracle-api
uv sync --group dev
uv run flask --app main run --debug
```

### Frontend
```bash
cd frontend/brick-oracle
npm install
npm run dev
```

Frontend runs on `http://localhost:5173`, proxying `/api` to `http://127.0.0.1:5000`.

## Repository Contents

- README.md
- WEEKLY_STATUS.md
- PAGE_TESTING.md
- SQL_TESTING.md
- FINAL_REPORT.md
- Presentation slides
- Demo video
- Source code (frontend and backend)
- Test cases

## Final Status Report

### What We Completed

- Catalog data layer: 17 tables, ~1.5M rows seeded from Rebrickable CSVs with SQLite immutability triggers
- User authentication: registration and login with password hashing
- Home page: stat cards and set carousel connected to real API
- Set Browser: theme/piece filtering, sorting, load-more pagination, fully connected to backend
- Set Builder (Brick Diff): set title from real API, brick grid with owned/partial/missing color coding, filter toggle
- Collection Browser: table view 
- Site header: search bar, navigation, auth-conditional login/logout
- Auth pages: login and registration with error handling
- Backend API: `GET /api/sets/`, `GET /api/sets/themes`, `GET /api/sets/:set_num`, `POST /api/auth/register`, `POST /api/auth/login`
- Project documentation: PAGE_TESTING.md, SQL_TESTING.md, feature table

### What We Were in the Middle of Implementing

- Brick Diff API: UI complete with mock data, backend diff calculation not yet wired up
- Header search: UI complete, no backend search endpoint
- Individual Set View: Set view has mock data but still needs to be connected to API
- Home stat cards: still hardcoded mock values
- Collection Storage Bins: database models exist, no frontend or API implementation
- Collection Modals: Add modal frontend is implemented, no backend is implemented. Upload, Delete, Edit modals are not implemented
- Collection Viewer: Frontend is implemented with mock data. We can add a record with add modal and it is reflected in the frontend. No data persists.

### What We Planned for the Future

- Set Recommendations based on collection completion percentage
- Importing of externally sourced Sets (from 3rd party builders & sites: Rebrickable, BrickLink, CSV) 
- Set completion price estimates using BrickLink market data
- Set Progress Tracker
- Collection sharing (public/private)
- User follow and notifications
- Collection Viewer / Modals: Implement the rest of the modals and connect with the backend.
- Collection Storage Bins: Allow the users to create “storage bins” for specific bricks and collections.
- 3D Set explorer
- Establish a design language and visual identity for the application aligned with modern standards

### Known Problems

- Auth token is user UUID, not a signed JWT, no server-side validation on protected routes
- Brick Diff displays mock data only
- Header search returns mock results only
- Home stat cards show hardcoded values
- Collection Viewer: Table is hardcoded with records
- Collection Modals: Add Modal frontend is implemented which mocks adding a record to the table

## System Overview

- **Frontend:** React 19 + TypeScript + TanStack Router + Vite
- **Backend:** Flask + SQLAlchemy
- **Database:** SQLite, seeded from Rebrickable CSV exports on first startup

The 12 catalog tables are immutable (enforced by SQLite triggers). The 5 user tables (users, collections, collection_parts, storage_bins, bin_parts) are fully mutable.

## Pages That Access Database Information

| Page | Tables Accessed |
| --- | --- |
| Home Page | `sets` |
| Auth | `users` |
| Set Browser | `sets`, `themes` |
| Set Builder | `sets`, `inventories`, `inventory_parts`, `parts`, `colors`, `collections`, `collection_parts` |
| Collection Browser | `users`, `collections`, `collection_parts`, `parts`, `colors` |
| Add Modal | `inventory_parts`, `parts`, `colors` |

## Page Data Access Tests

### Use Case: Set Browser loads sets with theme filter

**Pre-conditions:** Backend running, catalog seeded  
**Test Steps:**
1. Navigate to `/sets`
2. Select "Star Wars" from the Theme dropdown

**Expected Result:** Only Star Wars sets appear  
**Status:** Pass

---

### Use Case: Unauthenticated user redirected from Collection Browser

**Pre-conditions:** No active session token  
**Test Steps:**
1. Navigate to `/collection` without logging in

**Expected Result:** User redirected to `/auth`  
**Status:** Pass

## Reflection

- **Immutable catalog layer** eliminated a class of data integrity bugs.
- **Vertical slices** let each person own their feature end-to-end without blocking others.
- **Mock data first** allowed frontend and backend to develop in parallel.
- **Scope control** kept the core features shippable on time.
