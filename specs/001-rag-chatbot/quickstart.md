# Quickstart: RAG Chatbot Setup

**Feature**: `001-rag-chatbot`
**Date**: 2026-03-22

This guide gets the RAG chatbot running locally in under 15 minutes.

---

## Prerequisites

- Node.js ≥ 20 (for Docusaurus frontend)
- Python 3.11+ with `pip`
- Accounts (free tier):
  - [Qdrant Cloud](https://cloud.qdrant.io) — create a cluster, get URL + API key
  - [Neon](https://neon.tech) — create a project, get connection string
  - [OpenAI](https://platform.openai.com) — API key with gpt-4o-mini + embedding access
  - (Optional) [xAI Grok](https://x.ai/api) — if using Grok instead of OpenAI

---

## Step 1: Clone & Configure Environment

```bash
# From repo root
cp backend/.env.example backend/.env
```

Edit `backend/.env`:
```env
# LLM Provider (choose one)
OPENAI_API_KEY=sk-...
OPENAI_BASE_URL=                          # leave blank for OpenAI; set to https://api.x.ai/v1 for Grok
OPENAI_MODEL=gpt-4o-mini

# Embeddings
EMBEDDING_MODEL=text-embedding-3-small
EMBEDDING_DIMENSIONS=1536

# Qdrant
QDRANT_URL=https://your-cluster.qdrant.io
QDRANT_API_KEY=your-qdrant-api-key
QDRANT_COLLECTION=physical-ai-book

# Neon Postgres (optional for base RAG)
NEON_DB_URL=postgresql://user:pass@ep-xxx.neon.tech/neondb?sslmode=require

# Backend
BACKEND_PORT=8000
BACKEND_CORS_ORIGINS=http://localhost:3000,https://PHYSICAL-AI-HUMANOID-ROBOTICS.vercel.app
ADMIN_SECRET=change-me-in-production

# RAG Tuning
TOP_K=6
MAX_HISTORY_TURNS=6
MAX_CHUNK_TOKENS=800
CHUNK_OVERLAP_TOKENS=100
```

---

## Step 2: Install Backend Dependencies

```bash
cd backend
python -m venv .venv
source .venv/bin/activate     # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

`requirements.txt` includes:
```
fastapi>=0.115.0
uvicorn[standard]>=0.30.0
openai>=1.50.0
qdrant-client>=1.12.0
python-frontmatter>=1.1.0
tiktoken>=0.8.0
pydantic>=2.9.0
python-dotenv>=1.0.0
slowapi>=0.1.9
httpx>=0.27.0
pytest>=8.3.0
pytest-asyncio>=0.24.0
httpx>=0.27.0
```

---

## Step 3: Run Document Ingestion

```bash
# From repo root (with backend venv active)
python backend/scripts/ingest.py

# Expected output:
# [ingest] Scanning docs/ ...
# [ingest] Found 27 markdown files across 10 chapters
# [ingest] Processing chapter-01-introduction/index.md → 4 chunks
# ...
# [ingest] Total: 27 files, 142 chunks, 142 embeddings
# [ingest] Upserted to Qdrant collection 'physical-ai-book' ✓
# [ingest] Duration: 45.2s
```

> Run ingestion whenever chapter content is updated. It is idempotent — safe to re-run.

---

## Step 4: Start Backend Server

```bash
cd backend
uvicorn main:app --reload --port 8000
```

Verify:
```bash
curl http://localhost:8000/health
# {"status":"ok","qdrant_connected":true,"version":"1.0.0"}
```

---

## Step 5: Configure Frontend

Edit `src/components/ChatWidget/config.ts`:
```typescript
export const CHAT_API_BASE =
  process.env.NODE_ENV === 'development'
    ? 'http://localhost:8000'
    : 'https://your-backend.railway.app';
```

Or use Docusaurus's `customFields` in `docusaurus.config.ts`:
```typescript
customFields: {
  chatApiBase: process.env.CHAT_API_BASE ?? 'http://localhost:8000',
},
```

---

## Step 6: Start Docusaurus

```bash
# From repo root
npm install
npm start
```

Open [http://localhost:3000](http://localhost:3000). The chat widget icon appears in the bottom-right corner of every page.

---

## Step 7: Test the Chatbot

**General Q&A**:
```
Open any chapter → Click chat icon → Type:
"What is ROS 2 and how does it relate to humanoid robots?"
→ Expected: Answer citing Chapter 3 — ROS 2 Basics
```

**Text Selection**:
```
Navigate to Chapter 7 → Select a paragraph → Chat widget shows selection context
→ Type: "Can you explain this in simpler terms?"
→ Expected: Answer scoped to Chapter 7 content
```

**Off-topic test** (should refuse gracefully):
```
"What is the capital of France?"
→ Expected: "This topic is not covered in the current textbook content."
```

---

## Deployment

### Backend → Railway

```bash
# Install Railway CLI
npm install -g @railway/cli
railway login
railway init
railway up
```

Set environment variables in Railway dashboard (all vars from `.env`).

### Frontend → Vercel (or GitHub Pages)

```bash
# Vercel
npx vercel --prod

# GitHub Pages
npm run build && npm run deploy
```

Ensure `CHAT_API_BASE` points to your Railway backend URL.

---

## Running Tests

```bash
cd backend
pytest tests/ -v

# Key test files:
# tests/test_chat.py    — /chat and /chat/selected endpoints
# tests/test_ingest.py  — ingestion pipeline unit tests
# tests/test_rag.py     — retrieval accuracy (requires Qdrant connection)
```

---

## Troubleshooting

| Issue | Fix |
|-------|-----|
| `QDRANT_URL` connection error | Check cluster is active on Qdrant Cloud dashboard |
| Empty citations in responses | Re-run ingestion; check collection has points |
| CORS error in browser | Add `http://localhost:3000` to `BACKEND_CORS_ORIGINS` |
| Widget not visible | Ensure `src/theme/Root.tsx` exists and imports `ChatWidget` |
| Streaming not working | Check browser supports `EventSource`; test with `curl -N` |
| Rate limit hit | Wait 1 minute; adjust `TOP_K` or `MAX_HISTORY_TURNS` to reduce tokens |
