"""POST /ingest — admin endpoint to trigger document ingestion pipeline."""
import os
from fastapi import APIRouter, HTTPException, Header

from models.schemas import IngestResponse

router = APIRouter()


@router.post("/ingest", response_model=IngestResponse)
async def trigger_ingest(
    x_admin_secret: str | None = Header(default=None),
) -> IngestResponse:
    """
    Triggers the full ingestion pipeline:
      walk docs/ → chunk → embed → upsert to Qdrant.

    Protected by X-Admin-Secret header.
    Idempotent — safe to call multiple times.
    """
    if x_admin_secret != os.getenv("ADMIN_SECRET"):
        raise HTTPException(status_code=403, detail="Invalid or missing admin secret")

    # Import here to avoid circular imports and allow lazy loading
    from scripts.ingest import run_ingestion

    repo_root = os.getenv("REPO_ROOT", ".")
    result = run_ingestion(docs_dir=os.path.join(repo_root, "docs"), repo_root=repo_root)
    return IngestResponse(**result)
