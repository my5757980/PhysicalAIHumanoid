---
id: 1
title: "Fix Backend OpenAI to Cohere"
stage: "integration"
date_iso: "2025-12-12"
surface: "agent"
model: "claude-sonnet-4-5-20250929"
feature: "002-rag-chatbot-integration"
branch: "002-rag-chatbot-integration"
user: "user"
command: "/sp.implement"
labels: ["backend", "cohere", "openai", "migration"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files_yaml: |
  - E:\New folder\PhysicalAIHumanoid\backend\main.py
  - E:\New folder\PhysicalAIHumanoid\backend\requirements.txt
tests_yaml: |
  - Test backend functionality after migration
outcome: "Successfully migrated backend from OpenAI to Cohere"
evaluation: "Backend now uses Cohere + Qdrant only, with no OpenAI dependencies"
---

# Fix Backend OpenAI to Cohere

## User Input
```
FINAL SPEC-KIT FIX PROMPT (Copy–Paste in Spec-Kit Plus)

PROMPT START ↓ ↓

You are an expert AI engineer.
Fix my backend so it uses Cohere + Qdrant only, and completely removes OpenAI from the project.

❗ My Problem:

The backend throws this error:

OpenAI: 401 Unauthorized
Incorrect API key provided


This happens because the backend still contains OpenAI code, but I am NOT using OpenAI.
I only want to use Cohere for chat + Cohere Embeddings + Qdrant for vector search.

❗ What I want:

Please update my backend code with the following requirements:

✔ REQUIREMENT 1 — REMOVE OPENAI COMPLETELY

Delete or comment-out:

from openai import OpenAI

OpenAI client initialization

Any client.chat.completions.create(...)

Any OpenAI streaming code

ANY OpenAI model calls

✔ REQUIREMENT 2 — USE COHERE FOR CHATTING (STREAMING)

Replace OpenAI chat completion with:

import cohere

co = cohere.Client(os.getenv("COHERE_API_KEY"))

response = co.chat(
    model="command-r-plus",
    message=final_prompt,
    stream=True
)


and stream tokens back to the frontend.

✔ REQUIREMENT 3 — USE COHERE EMBEDDINGS + QDRANT

Embedding code must be:

embed = co.embed(
    texts=[query],
    model="embed-english-v3.0"
).embeddings[0]


Qdrant vector search must stay same.

✔ REQUIREMENT 4 — UPDATE THE FUNCTION

Please fix/update this function so it works fully with Cohere:

async def ask_stream(request: Request):


It should:

Receive user question

Create Cohere embedding

Search Qdrant

Build final prompt

Generate streaming response using Cohere

Yield tokens back to frontend

✔ REQUIREMENT 5 — RETURN CLEAN FINAL WORKING CODE

Return the clean, final, fixed main.py file — ONLY using:

Cohere

Qdrant

FastAPI

Streaming

No OpenAI anywhere.
```

## Response
Successfully updated the backend to use Cohere + Qdrant only, completely removing OpenAI:

### 1. Removed OpenAI Completely
- Deleted `import openai`
- Removed `OPENAI_API_KEY` environment variable
- Removed `openai_client = openai.OpenAI(...)` initialization

### 2. Updated Embedding Function
- Changed from `embed-multilingual-v3.0` to `embed-english-v3.0` as required
- Updated to use Cohere embedding format: `co.embed(texts=[query], model="embed-english-v3.0").embeddings[0]`

### 3. Updated ask_stream Function
- Renamed function to `ask_stream` as required
- Replaced OpenAI streaming with Cohere streaming:
  - `co.chat(model="command-r-plus", message=final_prompt, stream=True)`
  - Updated to handle Cohere streaming events properly
- Updated error handling to reflect Cohere errors instead of OpenAI errors

### 4. Updated ask_question Function
- Replaced OpenAI completion with Cohere completion:
  - `co.chat(model="command-r-plus", message=final_prompt, temperature=request.temperature)`
  - Updated to use `response.text` instead of `response.choices[0].message.content`

### 5. Updated Requirements
- Removed `openai==1.52.0` from requirements.txt
- Kept all other dependencies (fastapi, uvicorn, qdrant-client, cohere, python-dotenv, pydantic)

### 6. Updated Health Check
- Removed "openai" status from health check endpoint
- Now only checks "cohere" and "qdrant" services

The backend now exclusively uses Cohere for chat and embeddings, and Qdrant for vector search, with no OpenAI dependencies remaining.