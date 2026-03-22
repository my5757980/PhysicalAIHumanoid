"""Neon Serverless Postgres client stub.

This module is a stub for the future auth/personalization bonus feature.
It does NOT establish a database connection in this base RAG implementation.

To activate (when auth bonus is implemented):
  1. pip install asyncpg
  2. Set NEON_DB_URL in .env
  3. Replace stub functions with real asyncpg calls
  4. Run migrations/001_initial_schema.sql against your Neon DB

Constitution §V: Neon Serverless Postgres is reserved for user metadata.
It is NOT used for RAG vector storage (Qdrant handles that exclusively).
"""


async def get_user_level(session_token: str) -> str | None:
    """
    Retrieve user's background level (sw_level) from Neon Postgres.

    Stub — returns None until auth bonus is implemented.
    When implemented: validates session_token → looks up users table → returns sw_level.

    Returns:
        "beginner" | "intermediate" | "advanced" | None
    """
    # TODO (T026/auth bonus): implement with asyncpg
    # async with asyncpg.connect(os.getenv("NEON_DB_URL")) as conn:
    #     row = await conn.fetchrow(
    #         "SELECT sw_level FROM users WHERE session_token = $1", session_token
    #     )
    #     return row["sw_level"] if row else None
    return None


async def log_message(
    conversation_id: str,
    role: str,
    content: str,
    citations: list,
) -> None:
    """
    Persist a chat message to Neon Postgres for cross-session history.

    Stub — no-op until auth bonus is implemented.
    """
    # TODO (T026/auth bonus): implement with asyncpg
    pass
