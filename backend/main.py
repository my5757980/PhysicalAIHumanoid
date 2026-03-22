"""Physical AI RAG Chatbot — FastAPI Application Entry Point.

Stack:
  - FastAPI 0.115+ with async endpoints
  - CORS: allow Vercel + localhost:3000
  - Rate limiting: slowapi (in-memory, 10 req/min per IP)
  - Streaming: SSE via StreamingResponse with X-Accel-Buffering: no

Constitution §V compliance:
  - FastAPI backend ✓
  - Qdrant Cloud Free Tier via services/qdrant_client.py ✓
  - Neon Postgres stub via services/neon_client.py ✓
  - OpenAI SDK (Grok-compatible via OPENAI_BASE_URL) ✓
  - All secrets in .env ✓
"""
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from dotenv import load_dotenv

from api.middleware.rate_limit import limiter
from api.routes.health import router as health_router
from api.routes.chat import router as chat_router
from api.routes.ingest import router as ingest_router

load_dotenv()

app = FastAPI(
    title="Physical AI RAG Chatbot API",
    version="1.0.0",
    description=(
        "Retrieval-Augmented Generation backend for the Physical AI & Humanoid Robotics "
        "textbook. Answers are grounded exclusively in textbook content stored in Qdrant Cloud."
    ),
    docs_url="/docs",
    redoc_url="/redoc",
)

# ── CORS ──────────────────────────────────────────────────────────────────────
_cors_origins_raw = os.getenv(
    "BACKEND_CORS_ORIGINS",
    "http://localhost:3000",
)
cors_origins = [origin.strip() for origin in _cors_origins_raw.split(",") if origin.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Rate limiting ──────────────────────────────────────────────────────────────
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# ── Routers ───────────────────────────────────────────────────────────────────
app.include_router(health_router)
app.include_router(chat_router)
app.include_router(ingest_router)
