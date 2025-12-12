---
id: 1
title: Update Plan With RAG Chatbot
stage: plan
date: 2025-12-11
surface: agent
model: Claude Sonnet 4.5
feature: 001-physical-ai-textbook
branch: 002-rag-chatbot-integration
user: ASFAR
command: /sp.phr
labels: ["plan", "rag", "chatbot", "integration"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - specs/001-physical-ai-textbook/plan.md
tests:
 - none
---

## Prompt

> /sp.plan is running…


Project Location:

The folder .specify/001-physical-ai-textbook/ already exists.

Task:

Update the existing "plan" file in this folder.
Do NOT create any new folders.
Do NOT delete or overwrite any existing content.
Append all new content **below** the current content in the plan file.

Content to add:

[PASTE THE NEW PLAN CONTENT HERE]



## Objective
Extend the PhysicalAIHumanoid textbook project with a fully integrated RAG chatbot inside the existing Docusaurus site.

## High-Level Plan

### Phase 1 — Backend Architecture
1. Create `backend/` folder inside PhysicalAIHumanoid (if not present).
2. Add:
   - `main.py` (FastAPI server)
   - `ingest_docs.py` (embedding + ingestion)
   - `utils.py` (chunking, embeddings, retrieval)
3. Configure:
   - Qdrant Cloud (collection: youtube-embedding)
   - Cohere embeddings API
   - Neon Postgres (optional logging)
4. Implement endpoints:
   - POST /ask
   - POST /embed
   - GET /health

### Phase 2 — Document Ingestion
1. Read markdown files from `/docs`
2. Chunk them (300–1200 tokens)
3. Add overlap (80–200 tokens)
4. Generate embeddings (Cohere)
5. Insert into Qdrant

### Phase 3 — Frontend Integration
1. Add `src/components/ChatWidget.jsx`
2. Add styling + floating icon
3. Modify `src/theme/Root.js` to load the widget globally
4. Connect frontend to backend `/ask` endpoint
5. Support:
   - text selection → priority RAG mode
   - streaming

### Phase 4 — Testing
1. Validate retrieval accuracy
2. Confirm no hallucinations
3. Confirm every answer cites book chunks

# END OF PLAN EXTENSION

## Response snapshot

Successfully updated the plan file in specs/001-physical-ai-textbook/plan.md by appending the RAG chatbot integration plan content as requested. The new content includes the objective to extend the PhysicalAIHumanoid textbook project with a fully integrated RAG chatbot and a high-level plan with four phases: Backend Architecture, Document Ingestion, Frontend Integration, and Testing.

## Outcome

- ✅ Impact: Plan file updated with RAG chatbot integration details
- 🧪 Tests: none
- 📁 Files: specs/001-physical-ai-textbook/plan.md
- 🔁 Next prompts: none
- 🧠 Reflection: Proper file location was identified (specs/ not .specify/) to successfully complete the task

## Evaluation notes (flywheel)

- Failure modes observed: Script .specify/scripts/bash/create-phr.sh does not exist, had to manually create PHR file using template
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Update documentation to include PowerShell script path if that's the intended approach on Windows