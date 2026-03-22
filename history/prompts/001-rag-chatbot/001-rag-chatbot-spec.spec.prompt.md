---
id: 001
title: RAG Chatbot Feature Specification
stage: spec
date: 2026-03-22
surface: agent
model: claude-sonnet-4-6
feature: 001-rag-chatbot
branch: 001-rag-chatbot
user: Muhammad Yaseen
command: /sp.specify
labels: ["rag", "chatbot", "docusaurus", "openai", "qdrant", "fastapi", "spec"]
links:
  spec: specs/001-rag-chatbot/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/001-rag-chatbot/spec.md
  - specs/001-rag-chatbot/checklists/requirements.md
  - history/prompts/001-rag-chatbot/001-rag-chatbot-spec.spec.prompt.md
tests:
  - Checklist validation: specs/001-rag-chatbot/checklists/requirements.md (all 13 items pass)
---

## Prompt

Add an integrated RAG chatbot to the existing Docusaurus-based Physical AI & Humanoid Robotics textbook.

Requirements:
- Embed a persistent chat widget (bottom-right, expandable) on every page using OpenAI ChatKit SDK style (React component).
- Support two modes: 1) General Q&A about full book content. 2) Context-specific answers based only on user-selected text (highlight text → ask about it).
- Backend: FastAPI server in /backend or /chatbot folder with endpoints (/chat, /rag-selected).
- Vector DB: Qdrant Cloud Free Tier exclusively for storing embeddings of all docs/*.md chapters (ingestion script to chunk, embed with OpenAI text-embedding-3-small, upsert to collection).
- LLM: Use OpenAI gpt-4o-mini (or compatible like Grok via base_url switch) for generation, always answer using retrieved context only + cite sources (chapter/section).
- Relational DB: Neon Serverless Postgres for user metadata if auth implemented (but focus on RAG first).
- Maintain conversation context (multi-turn).
- Handle text selection: JS to capture selected text, send to backend with question.
- Follow constitution: Use existing stack (FastAPI, Qdrant, Neon), no Docusaurus branding, clean UI.
- Bonus consideration: Prepare hooks for personalization/Urdu if later.
- Output: Full feature specification with testable acceptance criteria.

## Response snapshot

Created a complete feature specification at `specs/001-rag-chatbot/spec.md` with:

- **5 prioritized user stories** (P1–P5): General Q&A, Text Selection Q&A, Multi-Turn Conversation, Source Citations, Document Ingestion — each independently testable.
- **18 functional requirements** (FR-001–FR-018) covering widget behavior, general Q&A backend, text-selection backend, ingestion pipeline, and conversation management.
- **5 key entities**: Message, Conversation, DocumentChunk, Citation, SelectionContext.
- **10 success criteria** (SC-001–SC-010) with measurable thresholds (10s response time, 90% citation rate, 10-exchange context window, 2s widget load, 10 concurrent sessions).
- **Constraints section** encoding constitutional tech stack mandates (FastAPI, Qdrant, gpt-4o-mini, text-embedding-3-small, Neon Postgres, React widget).
- **Non-Goals** explicitly excluding auth, Urdu translation, personalization, voice input, and admin dashboard.
- **Checklist** at `specs/001-rag-chatbot/checklists/requirements.md` — all 13 items pass, zero clarifications needed.

## Outcome

- ✅ Impact: Full RAG chatbot specification ready for `/sp.plan` — covers all hackathon base-functionality requirements for the chatbot component.
- 🧪 Tests: Spec checklist validated (13/13 pass, 1 iteration).
- 📁 Files: specs/001-rag-chatbot/spec.md, specs/001-rag-chatbot/checklists/requirements.md
- 🔁 Next prompts: `/sp.plan` to design API contracts, component architecture, and deployment topology.
- 🧠 Reflection: User description was detailed and aligned with the constitution — zero clarifications needed. Tech stack constraints encoded in a dedicated Constraints section rather than embedded in FRs, keeping requirements user-facing while preserving the mandated stack for planning.

## Evaluation notes (flywheel)

- Failure modes observed: Git repo has no initial commit (HEAD unborn) — branch creation skipped; created directory structure manually. Script ran but failed on git checkout; file creation succeeded via agent-native tools.
- Graders run and results (PASS/FAIL): Spec checklist — PASS (13/13)
- Prompt variant (if applicable): Full user-provided requirements with explicit tech stack
- Next experiment: Test whether splitting Constraints into a separate appendix vs. inline improves plan phase accuracy
