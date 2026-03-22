---
id: 002
title: RAG Chatbot Implementation Plan
stage: plan
date: 2026-03-22
surface: agent
model: claude-sonnet-4-6
feature: 001-rag-chatbot
branch: 001-rag-chatbot
user: Muhammad Yaseen
command: /sp.plan
labels: ["rag", "chatbot", "fastapi", "qdrant", "docusaurus", "architecture", "plan"]
links:
  spec: specs/001-rag-chatbot/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/001-rag-chatbot/plan.md
  - specs/001-rag-chatbot/research.md
  - specs/001-rag-chatbot/data-model.md
  - specs/001-rag-chatbot/quickstart.md
  - specs/001-rag-chatbot/contracts/openapi.yaml
  - history/prompts/001-rag-chatbot/002-rag-chatbot-plan.plan.prompt.md
tests:
  - Constitution check: all 11 gates pass (plan.md Constitution Check table)
---

## Prompt

Plan the technical implementation for adding the integrated RAG chatbot to the existing Docusaurus-based Physical AI & Humanoid Robotics textbook, strictly following the constitution (stack: FastAPI backend, Qdrant Cloud Free Tier for vector DB, Neon Serverless Postgres for user metadata if needed, OpenAI Agents SDK + ChatKit for orchestration and UI widget).

Key technical decisions:
- Frontend: Embed persistent React-based chat widget (bottom-right floating, expandable/collapsible, with text selection support) into Docusaurus via custom theme/Root.tsx or plugin. Use ChatKit SDK style for beautiful UI (markdown support, typing indicator, message history).
- Backend: FastAPI server in /backend or /chatbot folder (Python 3.11+), with async endpoints: /chat (general Q&A), /chat/selected (for highlighted text context).
- RAG Pipeline:
  - Ingestion: Script (scripts/ingest.py) to load all docs/*.md files, chunk them (recursive character splitter or markdown-aware), generate embeddings with OpenAI text-embedding-3-small (or Grok-compatible if switched), upsert to Qdrant collection (named e.g. "physical-ai-book").
  - Retrieval: Qdrant hybrid search (vector + keyword if possible), top-k=5-8 chunks, with metadata (chapter, section) for citations.
  - Generation: OpenAI gpt-4o-mini (or Grok via base_url switch in .env) with system prompt to answer only from context, cite sources (e.g. "From Chapter X: ..."), maintain conversation history (store in session or Neon if auth).
- Databases: Qdrant exclusively for RAG vectors/embeddings. Neon Postgres only for future auth/personalization (user prefs, background data) — keep minimal for base RAG.
- Integration: Widget makes API calls to FastAPI (CORS enabled), selected text captured via JS window.getSelection() and sent as context.
- Deployment: Frontend on GitHub Pages (static), backend on Railway/Render/Hugging Face (free), Qdrant/Neon cloud free tiers.
- Security: .env for all keys (OPENAI_API_KEY or xAI equivalent, QDRANT_URL, NEON_DB_URL), no hardcoding.
- Bonus prep: Add hooks for personalization (prompt modifier based on user background) and Urdu translation (future LLM call or cached).
- Code quality: Type hints in Python, ESLint/Prettier in frontend, tests for API endpoints.
- Folder structure updates: Add /backend, /scripts, src/components/ChatWidget.tsx, etc.

Generate a detailed plan.md with architecture diagram description (text-based), component breakdown, data flow, tech choices justification, risks/mitigations, and quickstart steps.

## Response snapshot

Generated 5 planning artifacts for `001-rag-chatbot`:

1. **plan.md** — Full architecture plan including:
   - ASCII architecture diagram (Browser → FastAPI → Qdrant/OpenAI/Neon)
   - Project structure (backend/ + src/theme/Root.tsx + src/components/ChatWidget/)
   - Three data flows: Ingestion, General Q&A (/chat), Text-Selection (/chat/selected)
   - Component design table (frontend) + RagService pseudocode (backend)
   - Citation-enforced system prompt template
   - Tech choices justification table (9 decisions)
   - Risk matrix (7 risks with mitigations)
   - 5-phase implementation overview (A=Backend, B=Ingestion, C=Widget, D=Tests, E=Bonus)
   - 3 ADR flags raised

2. **research.md** — Phase 0 decisions on: Root.tsx injection, text selection capture, Qdrant schema, FastAPI SSE streaming, citation enforcement, ingestion chunking, deployment architecture, bonus hooks

3. **data-model.md** — Entity diagrams, Qdrant collection schema, Pydantic v2 models (ChatRequest, ChatResponse, StreamChunk), TypeScript interfaces, Neon Postgres stub schema, UUID5 ID derivation, context window budget table

4. **quickstart.md** — Step-by-step local setup (7 steps), deployment guide (Railway + Vercel), troubleshooting table

5. **contracts/openapi.yaml** — OpenAPI 3.1 spec for /health, /chat, /chat/selected, /ingest endpoints with full request/response schemas

Constitution check: 11/11 gates pass. 3 ADR suggestions surfaced.

## Outcome

- ✅ Impact: Complete technical plan ready for /sp.tasks — all architectural decisions resolved, all 18 FRs mapped to implementation phases.
- 🧪 Tests: Constitution check 11/11 pass; backend test strategy defined (pytest, 3 test files)
- 📁 Files: plan.md, research.md, data-model.md, quickstart.md, contracts/openapi.yaml
- 🔁 Next prompts: /sp.tasks to generate ordered implementation tasks; /sp.adr for 3 flagged decisions
- 🧠 Reflection: Key insight — client-side history state (stateless backend) is essential for free-tier deployment; SSE via Fetch+ReadableStream is required because EventSource doesn't support POST bodies.

## Evaluation notes (flywheel)

- Failure modes observed: setup-plan.ps1 returned incorrect repo root path (E:\New folder\ instead of E:\New folder\New folder\yaseen\); worked around by using correct paths directly.
- Graders run and results (PASS/FAIL): Constitution check — PASS (11/11)
- Prompt variant (if applicable): User provided detailed technical decisions inline with /sp.plan
- Next experiment: Test whether splitting ingestion into a separate /sp.specify feature vs embedding in same feature improves task granularity
