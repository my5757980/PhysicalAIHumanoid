-- Neon Serverless Postgres schema
-- Feature: 001-rag-chatbot (auth/personalization bonus hooks)
-- Run against your Neon database: psql $NEON_DB_URL -f migrations/001_initial_schema.sql
--
-- NOTE: This schema is a stub for future bonus features.
-- The base RAG chatbot does NOT require this database.
-- Activate when implementing: Authentication (50pts) + Personalization (50pts)

CREATE TABLE IF NOT EXISTS users (
    id         UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email      TEXT UNIQUE NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    -- Background collected at signup (better-auth bonus)
    sw_level   TEXT CHECK (sw_level IN ('beginner', 'intermediate', 'advanced')),
    hw_level   TEXT CHECK (hw_level IN ('beginner', 'intermediate', 'advanced'))
);

CREATE TABLE IF NOT EXISTS conversations (
    id         UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id    UUID REFERENCES users (id) ON DELETE CASCADE,
    session_id TEXT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS chat_messages (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    conversation_id UUID REFERENCES conversations (id) ON DELETE CASCADE,
    role            TEXT NOT NULL CHECK (role IN ('user', 'assistant')),
    content         TEXT NOT NULL,
    citations       JSONB,
    created_at      TIMESTAMPTZ DEFAULT NOW()
);

-- Index for fast session lookup
CREATE INDEX IF NOT EXISTS idx_conversations_session ON conversations (session_id);
CREATE INDEX IF NOT EXISTS idx_messages_conversation ON chat_messages (conversation_id);
