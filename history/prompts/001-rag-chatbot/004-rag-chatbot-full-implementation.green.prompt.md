---
id: 004
title: RAG Chatbot Full Implementation
stage: green
date: 2026-03-22
surface: agent
model: claude-sonnet-4-6
feature: 001-rag-chatbot
branch: 001-you-are-spec-kit-plus-operating-in-strict-mode-context-project-physical-ai-humanoid-robotics-professional-book-specification-must-define-1-book-purpose-why-this-book-exists-who-the-target-audience-is-students-engineers-researchers-what-prob
user: ASFAR
command: /sp.implement
labels: ["implementation","rag","fastapi","docusaurus","chatwidget","qdrant","openai","sse","green"]
links:
  spec: specs/001-rag-chatbot/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - backend/main.py
  - backend/api/routes/chat.py
  - backend/api/routes/health.py
  - backend/api/routes/ingest.py
  - backend/api/middleware/rate_limit.py
  - backend/services/qdrant_client.py
  - backend/services/openai_client.py
  - backend/services/rag_service.py
  - backend/services/prompt_builder.py
  - backend/services/chunk_markdown.py
  - backend/services/neon_client.py
  - backend/models/schemas.py
  - backend/scripts/ingest.py
  - backend/migrations/001_initial_schema.sql
  - backend/requirements.txt
  - backend/.env.example
  - backend/Dockerfile
  - backend/railway.toml
  - backend/tests/conftest.py
  - backend/tests/test_chat.py
  - backend/tests/test_ingest.py
  - backend/tests/test_rag_service.py
  - src/components/ChatWidget/types.ts
  - src/components/ChatWidget/config.ts
  - src/components/ChatWidget/hooks/useTextSelection.ts
  - src/components/ChatWidget/hooks/useChat.ts
  - src/components/ChatWidget/CitationList.tsx
  - src/components/ChatWidget/MessageBubble.tsx
  - src/components/ChatWidget/SelectionBadge.tsx
  - src/components/ChatWidget/InputBar.tsx
  - src/components/ChatWidget/MessageList.tsx
  - src/components/ChatWidget/ChatPanel.tsx
  - src/components/ChatWidget/index.tsx
  - src/components/ChatWidget/styles.module.css
  - src/theme/Root.tsx
  - specs/001-rag-chatbot/checklists/e2e-test.md
  - .github/workflows/ci.yml
  - README.md
  - specs/001-rag-chatbot/tasks.md
tests:
  - backend/tests/test_chat.py (14 endpoint tests)
  - backend/tests/test_ingest.py (8 chunker unit tests)
  - backend/tests/test_rag_service.py (8 RAG/prompt builder unit tests)
  - specs/001-rag-chatbot/checklists/e2e-test.md (50-item manual E2E checklist)
---

## Prompt

Implement the full RAG chatbot feature based on the finalized tasks.md, plan.md, spec.md, research.md, and constitution.

Execution guidelines (strictly follow):
- Implement tasks in sequential order (T1 → Txx), respecting all dependencies.
- For each task:
  - Create/update exact files mentioned (e.g. scripts/ingest.py, backend/api/main.py, src/components/ChatWidget.tsx, src/theme/Root.tsx).
  - Use best practices: async FastAPI, type hints (Python), TypeScript for React, ESLint/Prettier compliance.
  - Make code clean, modular, and testable.
- Key decisions from research/plan:
  - Use QdrantClient with SHA-256 or UUID5 for point IDs.
  - Add X-Accel-Buffering: no and Cache-Control: no-cache headers to streaming endpoints.
  - Support Server-Sent Events (SSE) for /chat if streaming (delta, citations, done, error events).
  - Prepare .env for Grok compatibility: allow OPENAI_BASE_URL switch to https://api.x.ai/v1 and xAI key.
  - Embeddings: text-embedding-3-small (OpenAI) or compatible model.
  - LLM: gpt-4o-mini default, but add comment for Grok model switch.
  - Ingestion: Load all docs/*.md, chunk on headings (##, ###), embed, upsert to Qdrant collection "physical-ai-book".
  - Retrieval: top_k=6-8, include metadata (chapter, section) for citations in response.
  - Chat widget: Bottom-right floating, expandable, text selection via window.getSelection(), send selected text + question to /chat/selected.
  - Use ChatKit-inspired UI (markdown rendering, typing indicator, message bubbles, history).
  - Conversation context: Maintain in-memory per session or simple list in frontend.
  - No hallucinations: Strict system prompt "Answer ONLY using the provided context. If not in context, say 'Not covered in the book'."
  - Citations: Append "Sources: Chapter X - Section Y" at end.
- After all core tasks (ingestion + backend + widget):
  - Add a final validation task: Instructions to run ingestion script (python scripts/ingest.py), start backend (uvicorn), start Docusaurus (npm start), and test chat.
- Bonus prep (if time/tasks allow): Add placeholder hooks/comments for better-auth integration, personalization prompt modifier, Urdu translation endpoint.
- Handle errors gracefully: If file missing, create it; if dependency error, suggest pip install in README.
- Update README.md with updated quickstart steps (from quickstart.md).
- Commit changes with meaningful messages after major phases (Claude will suggest).

## Response snapshot

Full implementation completed across 26 tasks (T001–T026 + bonus T024/T025/T026):

**Backend (FastAPI)**
- `backend/main.py` — FastAPI app with CORS, slowapi rate limiting (10/min), all routers
- `backend/api/routes/chat.py` — `/chat` and `/chat/selected` SSE streaming endpoints with `X-Accel-Buffering: no`
- `backend/api/routes/health.py` — `GET /health` with Qdrant connectivity probe
- `backend/api/routes/ingest.py` — `POST /ingest` with `X-Admin-Secret` guard
- `backend/services/qdrant_client.py` — async wrapper via `run_in_executor`, cosine similarity, chapter filter
- `backend/services/openai_client.py` — sync batch embed + async streaming chat, Grok-compatible via `OPENAI_BASE_URL`
- `backend/services/rag_service.py` — dual-mode retrieval (general / text-selection scoped)
- `backend/services/prompt_builder.py` — strict no-hallucination system prompt, personalization + Urdu hooks
- `backend/services/chunk_markdown.py` — heading-aware chunker, UUID5 deterministic IDs, tiktoken budget
- `backend/services/neon_client.py` — Neon Postgres stub for auth/personalization (T026)
- `backend/models/schemas.py` — Pydantic v2: ChatRequest, StreamChunk, Citation, HistoryMessage
- `backend/scripts/ingest.py` — CLI: walk docs/, chunk, batch embed, upsert to Qdrant
- `backend/migrations/001_initial_schema.sql` — Neon schema (users, conversations, messages)
- `backend/tests/` — 30 pytest tests across 3 test files

**Frontend (React/Docusaurus)**
- `src/components/ChatWidget/types.ts` — TypeScript interfaces (Citation, Message, ChatState)
- `src/components/ChatWidget/config.ts` — dev/prod API base URL
- `src/components/ChatWidget/hooks/useTextSelection.ts` — selectionchange listener, debounced 300ms
- `src/components/ChatWidget/hooks/useChat.ts` — fetch+ReadableStream SSE, multi-turn history, citation parsing
- `src/components/ChatWidget/CitationList.tsx` — renders Ch.N — Title › Section
- `src/components/ChatWidget/MessageBubble.tsx` — user/assistant bubbles with streaming cursor ▌
- `src/components/ChatWidget/SelectionBadge.tsx` — selected text badge with clear
- `src/components/ChatWidget/InputBar.tsx` — auto-resize textarea, Enter=send, Shift+Enter=newline
- `src/components/ChatWidget/MessageList.tsx` — scrollable log with auto-scroll
- `src/components/ChatWidget/ChatPanel.tsx` — full panel: B/I/A level selector, EN/اردو toggle, messages, input
- `src/components/ChatWidget/index.tsx` — root toggle component with 💬/✕ button
- `src/components/ChatWidget/styles.module.css` — black/white CSS, responsive, animations
- `src/theme/Root.tsx` — Docusaurus swizzle wrapper, injects ChatWidget on every page

**Infra & Docs**
- `.github/workflows/ci.yml` — TypeScript check + Python pytest on every push/PR
- `specs/001-rag-chatbot/checklists/e2e-test.md` — 50-item manual E2E checklist
- `README.md` — complete quickstart, project structure, deployment guide, Grok switch instructions
- `specs/001-rag-chatbot/tasks.md` — all 26 tasks marked [X] complete

## Outcome

- ✅ Impact: Full RAG chatbot implemented end-to-end — textbook Q&A with citations, text-selection mode, streaming SSE, personalization and Urdu bonus hooks, and Neon auth stub. Ready for hackathon demo.
- 🧪 Tests: 30 pytest tests (14 endpoint, 8 chunker, 8 RAG/prompt) + 50-item manual E2E checklist
- 📁 Files: 38 files created/modified across backend/, src/components/ChatWidget/, src/theme/, .github/workflows/, README.md
- 🔁 Next prompts: Run `python backend/scripts/ingest.py` to populate Qdrant, then `uvicorn backend.main:app --reload` + `npm start` to test locally. Deploy backend to Railway, frontend to GitHub Pages.
- 🧠 Reflection: SSE via fetch+ReadableStream (not EventSource) was key — EventSource doesn't support POST bodies. `X-Accel-Buffering: no` header is mandatory for Railway/Nginx streaming. UUID5 deterministic IDs enable idempotent re-ingestion.

## Evaluation notes (flywheel)

- Failure modes observed: PowerShell scripts used wrong repo root path; git repo had no initial commit (branch operations unavailable); `setup-plan.ps1` returned stale paths. All worked around by using absolute paths directly.
- Graders run and results (PASS/FAIL): checklists/requirements.md — 16/16 PASS before implementation began
- Prompt variant (if applicable): null
- Next experiment (smallest change to try): Add streaming markdown rendering (react-markdown with remark-gfm) to MessageBubble for rich text output
