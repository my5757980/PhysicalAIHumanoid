# Physical AI & Humanoid Robotics — Interactive Textbook

An AI-native textbook for Physical AI & Humanoid Robotics, built with Docusaurus v3 and powered by a RAG (Retrieval-Augmented Generation) chatbot for intelligent Q&A.

---

## Features

- **Persistent chat widget** — floating bottom-right assistant on every page
- **Text selection mode** — highlight any passage, then ask questions about it
- **RAG pipeline** — answers grounded strictly in textbook content (no hallucinations)
- **Source citations** — every answer cites the chapter and section
- **Multi-turn conversations** — maintains context across the session
- **Personalization** — Beginner / Intermediate / Advanced explanation depth
- **Urdu translation** — toggle EN ↔ اردو responses

---

## Quickstart

### Prerequisites

| Tool | Version |
|------|---------|
| Node.js | ≥ 18 |
| Python | ≥ 3.11 |
| npm | ≥ 9 |

### 1. Clone & install frontend

```bash
git clone <repo-url>
cd <repo>
npm install
```

### 2. Configure backend environment

```bash
cp backend/.env.example backend/.env
```

Edit `backend/.env` and fill in:

```env
OPENAI_API_KEY=sk-...          # OpenAI key (or xAI key for Grok)
QDRANT_URL=https://...         # Qdrant Cloud cluster URL
QDRANT_API_KEY=...             # Qdrant API key
# Optional: switch to Grok
# OPENAI_BASE_URL=https://api.x.ai/v1
# OPENAI_MODEL=grok-3-mini
```

### 3. Install backend dependencies

```bash
pip install -r backend/requirements.txt
```

### 4. Ingest textbook content

```bash
python backend/scripts/ingest.py
```

This chunks all `docs/**/*.md` files, embeds them with `text-embedding-3-small`, and upserts to the `physical-ai-book` Qdrant collection.

### 5. Start the backend

```bash
uvicorn backend.main:app --reload --port 8000
```

Verify: `curl http://localhost:8000/health` → `{"status":"ok","qdrant":"connected"}`

### 6. Start Docusaurus

```bash
npm start
```

Open [http://localhost:3000](http://localhost:3000) — the chat widget appears in the bottom-right corner.

---

## Running Backend Tests

```bash
pytest backend/tests/ -v
```

---

## Project Structure

```
.
├── docs/                    # Textbook Markdown chapters
├── src/
│   ├── components/
│   │   └── ChatWidget/      # React chat widget (all sub-components)
│   └── theme/
│       └── Root.tsx         # Docusaurus swizzle — injects widget site-wide
├── backend/
│   ├── main.py              # FastAPI app entry point
│   ├── api/routes/          # /chat, /chat/selected, /health, /ingest
│   ├── services/            # RAG pipeline, embeddings, Qdrant, prompt builder
│   ├── models/schemas.py    # Pydantic v2 request/response models
│   ├── scripts/ingest.py    # One-time ingestion CLI
│   ├── tests/               # pytest unit tests
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .env.example
├── specs/001-rag-chatbot/   # SDD artifacts (spec, plan, tasks, contracts)
└── .github/workflows/
    ├── ci.yml               # TypeScript check + Python tests
    └── deploy.yml           # GitHub Pages deployment
```

---

## Deployment

### Backend (Railway / Render)

1. Push `backend/` to your Railway/Render project
2. Set environment variables (same as `.env.example`)
3. Set `CORS_ORIGINS` to your GitHub Pages URL
4. Update `src/components/ChatWidget/config.ts` → `PROD_API_URL` with the backend URL

### Frontend (GitHub Pages)

```bash
npm run build
# GitHub Actions (deploy.yml) auto-deploys on push to main
```

---

## Architecture

```
Browser (Docusaurus)
  └── ChatWidget (React)
        ├── useTextSelection()  →  window.getSelection()
        ├── useChat()           →  fetch + ReadableStream (SSE)
        └── ChatPanel / MessageBubble / CitationList

FastAPI Backend
  ├── POST /chat              →  general Q&A (SSE stream)
  ├── POST /chat/selected     →  text-selection mode (SSE stream)
  └── POST /ingest            →  admin ingestion trigger

RAG Pipeline
  ├── Qdrant Cloud (vectors)  →  physical-ai-book collection
  ├── OpenAI text-embedding-3-small  →  1536-dim embeddings
  └── OpenAI gpt-4o-mini      →  streaming generation
```

---

## Switching to Grok (xAI)

In `backend/.env`:

```env
OPENAI_BASE_URL=https://api.x.ai/v1
OPENAI_API_KEY=xai-...
OPENAI_MODEL=grok-3-mini
```

The backend is fully compatible with xAI's OpenAI-compatible API.
"# PhysicalAIHumanoid" 
