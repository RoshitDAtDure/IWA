# Backend Endpoint Creation Protocol

This protocol defines the **standard procedure for creating backend endpoints** for the IC pipeline system.  
All endpoints must follow this protocol to ensure consistency, correctness, and auditability.

This protocol aligns strictly with the approved backend implementation plan.

---

## 1. Pre-Implementation Checklist (Mandatory)

Before writing an endpoint:

- Identify the **phase** the endpoint belongs to (Auth, Deal, IC Memo, etc.)
- Identify **allowed roles**
- Identify **read vs write** behavior
- Identify **tables impacted**
- Confirm whether the endpoint:
  - Mutates state
  - Requires audit logging
  - Requires versioning
  - Requires transactional safety

No endpoint is implemented without completing this checklist.

---

## 2. Endpoint Definition Contract

Every endpoint must define:

- HTTP method
- URL path
- Request schema
- Response schema
- Auth dependency
- Role guard
- DB session dependency

Endpoints without explicit contracts are invalid.

---

## 3. Standard Endpoint Creation Steps

### Step 1 — Permission Gate
- Attach `get_current_user`
- Attach role guard (`ADMIN`, `ANALYST`, `PARTNER`)
- Reject unauthorized access before DB interaction

**Impact**
- Prevents invalid state mutation
- Enforces domain authority at API boundary

---

### Step 2 — Input Validation
- Validate enums explicitly
- Validate entity existence (deal, memo, user)
- Validate ownership if applicable

**Impact**
- Prevents silent data corruption
- Prevents orphaned records

---

### Step 3 — Database Interaction
- Use a single DB session
- For write operations:
  - Wrap in transaction
  - Lock row if concurrency-sensitive
- Never partially commit state

**Impact**
- Guarantees atomicity
- Ensures consistency under concurrent access

---

### Step 4 — Side-Effect Handling
Apply **only if required**:

| Operation Type | Required Side Effect |
|---------------|---------------------|
| Deal stage change | Activity log |
| IC memo update | New memo version |
| Vote submission | Enforce uniqueness |
| User update | Timestamp update |

Side effects must occur in the **same transaction**.

**Impact**
- Preserves auditability
- Prevents desynchronization

---

### Step 5 — Persistence
- Commit transaction only after all side effects succeed
- Rollback on any failure

**Impact**
- Prevents partial writes
- Maintains referential integrity

---

### Step 6 — Response Construction
- Return only required fields
- Never expose internal IDs unnecessarily
- Maintain consistent response shape

**Impact**
- Stable frontend integration
- Reduced coupling

---

## 4. Database Impact Rules

### Read Endpoints
- No DB mutations
- No timestamps updated
- No audit entries

### Write Endpoints
Must explicitly document:
- Tables written
- Rows inserted/updated
- Constraints enforced
- Indexes relied upon

No undocumented DB mutation is allowed.

---

## 5. Endpoint Categories & Special Rules

### Auth Endpoints
- Never return password hash
- JWT payload limited to user_id + role
- No DB writes after login

---

### Deal Endpoints
- Stage transitions must be explicit
- Stage changes always generate Activity row
- `updated_at` must be updated

---

### Activity Endpoints
- Read-only
- Sorted by `created_at DESC`

---

### IC Memo Endpoints
- One memo per deal enforced at DB level
- Every save creates a new version
- Older versions immutable

---

### Comment Endpoints
- Partner-only creation
- No edits or deletes
- Append-only model

---

### Vote Endpoints
- One vote per user per deal
- Upsert allowed only if explicitly intended
- Vote changes must be deliberate

---

## 6. Error Handling Rules

- 401: Unauthenticated
- 403: Unauthorized role
- 404: Resource not found
- 409: Constraint violation
- 422: Validation failure

Errors must be explicit and deterministic.

---

## 7. Documentation Requirement

For every endpoint, update:
- README (if public-facing)
- Inline docstring describing:
  - Purpose
  - Role access
  - DB impact
  - Side effects

Endpoints without documentation are incomplete.

---

## 8. Completion Criteria

An endpoint is considered complete only if:
- Permissions enforced
- DB effects documented
- Side effects verified
- Error paths handled
- Matches implementation plan phase

---

## Non-Negotiable Rules

- No endpoint without auth
- No state change without audit or versioning
- No hidden DB mutations
- No role logic in frontend

This protocol is binding for all backend development.
