# Take-Home Assignment – High-Level Implementation Plan

## Phase 0 — Ground Rules (30 min)
- Create public GitHub repository
- Decide minimal scope: correctness > completeness
- Define enums: Roles, DealStages
- Commit empty backend + frontend folders

---

## Phase 1 — Backend Skeleton (2–3 hrs)
- Initialize FastAPI app
- Setup DB connection (Postgres / SQLite)
- Configure SQLAlchemy + Alembic
- User model with roles
- JWT-based auth (register/login)
- Role-based access guards

**Output:** authenticated API with role enforcement

---

## Phase 2 — Core Domain Models (2 hrs)
- Deal model with stage enum
- Activity model
- IC Memo + MemoVersion models
- Comment + Vote models
- Run migrations

**Output:** stable schema

---

## Phase 3 — Deal Pipeline APIs (2–3 hrs)
- Create deal
- Update deal
- Change deal stage
- Log Activity on every stage change (transactional)
- List deals by stage

**Output:** pipeline logic complete

---

## Phase 4 — IC Memo APIs (2 hrs)
- Create/update memo
- On save → create new version (full snapshot)
- Fetch version history
- Fetch specific version (read-only)

**Output:** versioned IC memo workflow

---

## Phase 5 — Frontend Setup (1 hr)
- React + Vite initialization
- Auth pages
- Token handling
- API client wrapper

**Output:** frontend-backend integration

---

## Phase 6 — Kanban Board UI (2–3 hrs)
- Fixed stage columns
- Deal cards
- Drag-and-drop support
- On drop → stage-change API call

**Output:** visual deal pipeline

---

## Phase 7 — Deal Detail Page (2 hrs)
- Deal metadata display
- IC memo editor (textarea / markdown)
- Version history list
- Read-only version viewer

**Output:** usable IC workflow

---

## Phase 8 — Partner Actions (1–2 hrs)
- Comments on deals
- Approve / Decline voting
- Permission checks

**Output:** governance loop complete

---

## Phase 9 — Polish & Submission (1 hr)
- README (setup, assumptions, trade-offs)
- Optional seed data
- Cleanup
- Final commit

---

## Non‑Negotiables
- Activity logging on stage changes
- Full snapshot memo versioning
- Server-side role enforcement
- App runs locally end-to-end
