---
id: 2
title: "Fix Cohere Streaming API Error"
stage: "red"
date_iso: "2025-12-12"
surface: "agent"
model: "claude-sonnet-4-5-20250929"
feature: "002-rag-chatbot-integration"
branch: "002-rag-chatbot-integration"
user: "user"
command: "/sp.implement"
labels: ["backend", "cohere", "streaming", "api"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files_yaml: |
  - E:\New folder\PhysicalAIHumanoid\backend\main.py
tests_yaml: |
  - Test streaming functionality after API fix
outcome: "Fixed Cohere streaming API call"
evaluation: "Backend now uses correct Cohere streaming method"
---

# Fix Cohere Streaming API Error

## User Input
```
E:\New folder\PhysicalAIHumanoid>python -m uvicorn backend.main:app --reload
←[32mINFO←[0m:     Will watch for changes in these directories: ['E:\\New folder\\PhysicalAIHumanoid']
←[32mINFO←[0m:     Uvicorn running on ←[1mhttp://127.0.0.1:8000←[0m (Press CTRL+C to quit)
←[32mINFO←[0m:     Started reloader process [←[36m←[1m2628←[0m] using ←[36m←[1mStatReload←[0m
C:\Users\ASFAR\AppData\Roaming\Python\Python314\site-packages\cohere\core\pydantic_utilities.py:13: UserWarning: Core Pydantic V1 functionality isn't compatible with Python 3.14 or greater.
  from pydantic.v1.datetime_parse import parse_date as parse_date
INFO:httpx:HTTP Request: GET https://a41eb234-d13f-4e96-a773-dcd9d5a81086.us-east4-0.gcp.cloud.qdrant.io:6333 "HTTP/1.1 200 OK"
←[32mINFO←[0m:     Started server process [←[36m5144←[0m]
←[32mINFO←[0m:     Waiting for application startup.
INFO:backend.main:Starting backend with Cohere + Qdrant
INFO:httpx:HTTP Request: GET https://a41eb234-d13f-4e96-a773-dcd9d5a81086.us-east4-0.gcp.cloud.qdrant.io:6333/collections "HTTP/1.1 200 OK"
INFO:backend.main:Qdrant collection physical_ai_docs exists
←[32mINFO←[0m:     Application startup complete.
←[32mINFO←[0m:     127.0.0.1:59598 - "←[1mOPTIONS /ask_stream HTTP/1.1←[0m" ←[32m200 OK←[0m
INFO:backend.main:Received streaming query: what is Physical AI & Humanoid Robotics
←[32mINFO←[0m:     127.0.0.1:59598 - "←[1mPOST /ask_stream HTTP/1.1←[0m" ←[32m200 OK←[0m
INFO:httpx:HTTP Request: POST https://api.cohere.com/v1/embed "HTTP/1.1 200 OK"
INFO:httpx:HTTP Request: POST https://a41eb234-d13f-4e96-a773-dcd9d5a81086.us-east4-0.gcp.cloud.qdrant.io:6333/collections/physical_ai_docs/points/scroll "HTTP/1.1 200 OK"
ERROR:backend.main:Cohere streaming error: Since python sdk cohere==5.0.0, you must now use chat_stream(...) instead of chat(stream=True, ...)
```

## Response
Fixed the Cohere streaming API error by updating the ask_stream function to use the correct method for Cohere SDK 5.0.0+:

### Changed:
- Updated `co.chat(model="command-r-plus", message=final_prompt, stream=True)` to `co.chat_stream(model="command-r-plus", message=final_prompt)`
- The Cohere SDK version 5.0.0+ requires using `chat_stream(...)` instead of `chat(..., stream=True)`
- Non-streaming calls in ask_question function remain unchanged as they work correctly