# Backend Endpoint Implementation Plan

This document defines the ordered, step-wise backend implementation plan to minimize rework and ensure continuous progress.

---

## Step 1 — Auth & Identity (Foundation)

Endpoints
- POST /auth/register
- POST /auth/login

Responsibilities
- Password hashing
- JWT generation
- User activation check
- Token payload includes user_id and role

Output
- Working authentication
- JWT-secured requests

---

## Step 2 — Auth Dependencies & Role Guards

Components
- get_current_user dependency
- require_role(role) guard

Usage
- Applied to all protected routes

Output
- Server-side role enforcement

---

## Step 3 — Deal Creation & Read

Endpoints
- POST /deals
- GET /deals
- GET /deals/{id}

Rules
- Analyst/Admin only
- owner_id = current user
- Default stage = SOURCED

Output
- Deals persisted and retrievable

---

## Step 4 — Deal Stage Transition + Activity Log

Endpoint
- PATCH /deals/{id}/stage

Rules
- Validate stage enum
- Update deal + insert activity in same transaction
- Activity message must be human-readable

Output
- Auditable pipeline movement

---

## Step 5 — Activity Read APIs

Endpoint
- GET /deals/{id}/activities

Rules
- Sorted by created_at descending

Output
- Full audit trail visibility

---

## Step 6 — IC Memo Creation

Endpoints
- POST /deals/{id}/ic-memo
- GET /deals/{id}/ic-memo

Rules
- Analyst/Admin only
- Enforce one memo per deal

Output
- IC memo container exists

---

## Step 7 — IC Memo Versioning

Endpoints
- POST /ic-memos/{id}/versions
- GET /ic-memos/{id}/versions
- GET /ic-memos/{id}/versions/{version_number}

Rules
- Auto-increment version_number
- Store full snapshot on every save
- Older versions are read-only

Output
- Versioned decision record

---

## Step 8 — Comments

Endpoints
- POST /deals/{id}/comments
- GET /deals/{id}/comments

Rules
- Partner-only write
- All authenticated users can read

Output
- Qualitative discussion layer

---

## Step 9 — Votes

Endpoints
- POST /deals/{id}/vote
- GET /deals/{id}/votes

Rules
- Partner-only
- One vote per user per deal
- Enforce unique constraint

Output
- Formal decision capture

---

## Step 10 — Admin User Management (Optional)

Endpoints
- GET /users
- PATCH /users/{id}

Rules
- Admin-only
- Activate/deactivate users

---

## Hard Constraints

- No endpoint without authentication
- No stage change without activity log
- No memo update without version insert
- All permissions enforced server-side
