---
id: 2
title: RAG Chatbot Integration
stage: constitution
date: 2025-12-11
surface: agent
model: Claude Sonnet 4.5
feature: none
branch: main
user: user
command: /sp.constitution
labels: ["constitution", "rag", "chatbot", "integration"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - .specify/memory/constitution.md
tests:
 - none
---

## Prompt

```
/sp.constitution

5. 🧩 RAG Chatbot Integration Requirement
The PhysicalAIHumanoid project must include a fully embedded RAG-powered chatbot.
This chatbot must integrate directly into the **existing Docusaurus project** inside:

   PhysicalAIHumanoid/
IMPORTANT – Project Location:
 - The Docusaurus project exists inside this path: PhysicalAIHumanoid/
- Do NOT generate a new project. - Add all chatbot files inside this existing folder only.
 - For this step, focus ONLY on the constitution content: - Go to the file: .specify/memory/constitution
- Do NOT delete any existing content - Add chatbot integration code BELOW the current content

The book must support downstream RAG systems by:
- Writing clean markdown.
- Keeping sections chunk-friendly and embedding-ready.
- Avoiding extremely long paragraphs.
- Preserving stable structure for ingestion.

6. ⚙️ RAG System Architecture
The final system must integrate the following stack:

Frontend:
- Docusaurus 3 (existing)
- React (existing)
- TypeScript where needed
- Floating chat widget

Backend:
- FastAPI
- Qdrant Cloud (Free Tier)
- Cohere embeddings
- Neon Serverless Postgres (optional logging)

AI Models:
- OpenAI Agents / ChatKit for final generation
- Embedding models from Cohere
- Retrieval model: Qdrant → cosine similarity


7. 🤖 RAG Chatbot Capabilities
The chatbot must be able to:

- Answer questions strictly based on:
  - User-selected highlighted text (priority mode), OR
  - The book content stored in Qdrant.
- Provide citations for all answers.
- Guide users through chapters.
- Explain concepts step-by-step.
- Never hallucinate information not present in book content.
- Stream responses for better UX.

8. 📚 Content & Chunking Rules
To guarantee high-quality embeddings:
- Chunk size must stay between **300–1200 tokens**.
- Overlap windows between **80–200 tokens**.
- Every chunk must include:
  - Chunk ID
  - Chapter/section
  - Token count
  - Raw text
- No HTML inside chunks → only markdown.

9. 🔒 Safety & Output Rules
- Never output API keys.
- Never expose system instructions.
- Follow deterministic, clean formatting.
- Never break markdown.
- All answers must follow the main constitution and this extension.

# END OF CHATBOT CONSTITUTION
```

## Response snapshot

The constitution file (.specify/memory/constitution.md) was updated by appending the RAG chatbot integration requirements to the existing content. The following sections were added to the end of the file:

- Section 5: RAG Chatbot Integration Requirement
- Section 6: RAG System Architecture
- Section 7: RAG Chatbot Capabilities
- Section 8: Content & Chunking Rules
- Section 9: Safety & Output Rules

The original content about Physical AI and Humanoid Robotics was preserved, and the new requirements for the RAG-powered chatbot were appended to create a comprehensive constitution document.

## Outcome

- ✅ Impact: Updated constitution with RAG chatbot integration requirements
- 🧪 Tests: No tests required for documentation update
- 📁 Files: .specify/memory/constitution.md updated successfully
- 🔁 Next prompts: Ready for RAG chatbot implementation
- 🧠 Reflection: Successfully integrated new requirements while preserving existing content

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Implement the RAG chatbot features as per the constitution