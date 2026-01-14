-- =========================
-- EXTENSIONS
-- =========================
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- =========================
-- ENUMS
-- =========================
CREATE TYPE user_role AS ENUM (
  'ADMIN',
  'ANALYST',
  'PARTNER'
);

CREATE TYPE deal_stage AS ENUM (
  'SOURCED',
  'SCREEN',
  'DILIGENCE',
  'IC',
  'INVESTED',
  'PASSED'
);

CREATE TYPE vote_type AS ENUM (
  'APPROVE',
  'DECLINE'
);

-- =========================
-- USERS (AUTH + ROLES)
-- =========================
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  email TEXT NOT NULL UNIQUE,
  password_hash TEXT NOT NULL,
  role user_role NOT NULL,
  is_active BOOLEAN NOT NULL DEFAULT TRUE,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- =========================
-- DEALS (PIPELINE)
-- =========================
CREATE TABLE deals (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  name TEXT NOT NULL,
  company_url TEXT,
  owner_id UUID NOT NULL REFERENCES users(id) ON DELETE RESTRICT,
  stage deal_stage NOT NULL,
  round TEXT,
  check_size NUMERIC(14,2),
  status TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX idx_deals_stage ON deals(stage);
CREATE INDEX idx_deals_owner ON deals(owner_id);

-- =========================
-- ACTIVITY LOG (AUDIT TRAIL)
-- =========================
CREATE TABLE activities (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  deal_id UUID NOT NULL REFERENCES deals(id) ON DELETE CASCADE,
  actor_id UUID NOT NULL REFERENCES users(id) ON DELETE RESTRICT,
  message TEXT NOT NULL,
  from_stage deal_stage,
  to_stage deal_stage,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX idx_activities_deal ON activities(deal_id);

-- =========================
-- IC MEMO (ONE PER DEAL)
-- =========================
CREATE TABLE ic_memos (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  deal_id UUID NOT NULL UNIQUE REFERENCES deals(id) ON DELETE CASCADE,
  created_by UUID NOT NULL REFERENCES users(id) ON DELETE RESTRICT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- =========================
-- IC MEMO VERSIONS (FULL SNAPSHOT)
-- =========================
CREATE TABLE ic_memo_versions (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  memo_id UUID NOT NULL REFERENCES ic_memos(id) ON DELETE CASCADE,
  version_number INTEGER NOT NULL,
  summary TEXT,
  market TEXT,
  product TEXT,
  traction TEXT,
  risks TEXT,
  open_questions TEXT,
  created_by UUID NOT NULL REFERENCES users(id) ON DELETE RESTRICT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  UNIQUE (memo_id, version_number)
);

CREATE INDEX idx_memo_versions_memo ON ic_memo_versions(memo_id);

-- =========================
-- COMMENTS (PARTNERS)
-- =========================
CREATE TABLE comments (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  deal_id UUID NOT NULL REFERENCES deals(id) ON DELETE CASCADE,
  author_id UUID NOT NULL REFERENCES users(id) ON DELETE RESTRICT,
  body TEXT NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX idx_comments_deal ON comments(deal_id);

-- =========================
-- VOTES (APPROVE / DECLINE)
-- =========================
CREATE TABLE votes (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  deal_id UUID NOT NULL REFERENCES deals(id) ON DELETE CASCADE,
  voter_id UUID NOT NULL REFERENCES users(id) ON DELETE RESTRICT,
  vote vote_type NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  UNIQUE (deal_id, voter_id)
);

CREATE INDEX idx_votes_deal ON votes(deal_id);