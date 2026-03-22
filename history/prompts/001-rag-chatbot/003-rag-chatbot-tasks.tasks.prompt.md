---
id: 003
title: RAG Chatbot Implementation Tasks
stage: tasks
date: 2026-03-22
surface: agent
model: claude-sonnet-4-6
feature: 001-rag-chatbot
branch: 001-rag-chatbot
user: Muhammad Yaseen
command: /sp.tasks
labels: ["rag", "chatbot", "tasks", "fastapi", "docusaurus", "qdrant", "openai"]
links:
  spec: specs/001-rag-chatbot/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/001-rag-chatbot/tasks.md
  - specs/001-rag-chatbot/checklists/e2e-test.md (created in T022)
  - history/prompts/001-rag-chatbot/003-rag-chatbot-tasks.tasks.prompt.md
tests:
  - All tasks include acceptance criteria checklists
  - Backend test suite defined in T014 (pytest, ≥60% coverage, mocked)
  - E2E smoke test defined in T022
---

## Prompt

Break down the RAG chatbot implementation plan into a detailed, ordered, dependency-aware list of executable tasks.

Strictly follow the constitution (Section V stack: FastAPI, Qdrant Cloud Free Tier exclusive for RAG vectors, Neon Postgres only for user metadata if auth later, OpenAI Agents SDK + ChatKit style), recent spec.md, and plan.md for this feature.

Task breakdown requirements:
- Make tasks atomic and small (each task completable in one /implement pass, testable independently).
- Number tasks sequentially (T1, T2, ...).
- Group into logical phases (e.g. Phase 1: Setup & Config, Phase 2: Ingestion Pipeline, Phase 3: Backend API & RAG Logic, Phase 4: Frontend Chat Widget Integration, Phase 5: Testing & Polish).
- Include dependencies (e.g. T5 depends on T3 and T4).
- Each task MUST have: Clear description, Acceptance criteria (testable checklist), Files to create/update, Key decisions or notes, Priority/phase.
- Prioritize: 1. Core RAG (ingestion + retrieval + generation), 2. Chat widget embed in Docusaurus, 3. Text selection support, 4. Citations/source linking, 5. Multi-turn context.
- Prepare for bonuses: Add placeholder tasks/hooks for auth (better-auth), personalization (prompt modifier from Neon user data), Urdu translation.
- Include setup tasks: Qdrant/Neon account creation reminders (manual), .env.example updates, dependencies install.
- Ensure code quality: Type hints, linting, basic tests where possible.
- Output: Full tasks.md with markdown table or numbered list, dependency graph (text-based), and quick validation steps.

## Response snapshot

Generated `specs/001-rag-chatbot/tasks.md` with 26 tasks across 6 phases:

- **Phase 1 (T001–T005)**: Backend scaffold, FastAPI app+CORS+rate limiting, Pydantic schemas, Qdrant service, OpenAI service
- **Phase 2 (T006–T009)**: Markdown chunker, ingestion CLI script, admin /ingest endpoint, ingestion unit tests
- **Phase 3 (T010–T014)**: RAG retrieve service, prompt builder (citation-enforced + bonus hooks wired), /chat SSE endpoint, /chat/selected endpoint, backend test suite
- **Phase 4 (T015–T021)**: TypeScript types/config, useTextSelection hook, useChat hook (Fetch+ReadableStream SSE), MessageBubble+CitationList, InputBar+SelectionBadge, ChatPanel+Widget assembly+CSS, Root.tsx global injection
- **Phase 5 (T022–T023)**: E2E smoke test checklist, Railway+Vercel deployment config + GitHub Actions CI
- **Phase 6 (T024–T026, Bonus)**: Personalization hook (user_level UI + localStorage), Urdu translation toggle, Neon Postgres schema stub + client

Key design decisions embedded in tasks:
- T017: Fetch+ReadableStream (not EventSource) for POST streaming
- T021: src/theme/Root.tsx (auto-discovered, no swizzle command needed)
- T011: Bonus hooks (user_level, translate_to) wired passively — activate when frontend sends them
- T004: run_in_executor for async-safe synchronous Qdrant SDK calls
- T007: UUID5 deterministic chunk IDs for idempotent ingestion
- T012: X-Accel-Buffering: no header for Railway/Nginx streaming

## Outcome

- ✅ Impact: 26 atomic tasks covering 100% of base RAG requirements (T001–T023) + 3 bonus hooks (T024–T026). Ready for /sp.implement.
- 🧪 Tests: T009 (ingestion unit tests), T014 (backend pytest ≥60% coverage), T022 (E2E smoke test checklist)
- 📁 Files: specs/001-rag-chatbot/tasks.md
- 🔁 Next prompts: /sp.implement to execute tasks sequentially
- 🧠 Reflection: Tasks include full implementation code in each description — /implement can execute them without ambiguity. Bonus hooks (T024-T026) are wired passively into existing code structures so they activate without requiring refactoring.

## Evaluation notes (flywheel)

- Failure modes observed: None — tasks template followed correctly, all 26 tasks have acceptance criteria
- Graders run and results (PASS/FAIL): Task completeness check — PASS (all 26 have description, AC, files, deps, priority)
- Prompt variant (if applicable): User specified 5-phase breakdown + bonus hooks explicitly
- Next experiment: Test whether embedding full implementation code in task descriptions speeds up /sp.implement or creates confusion
