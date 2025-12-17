---
id: 3
title: "Update Cohere Model to Supported Version"
stage: "red"
date_iso: "2025-12-12"
surface: "agent"
model: "claude-sonnet-4-5-20250929"
feature: "002-rag-chatbot-integration"
branch: "002-rag-chatbot-integration"
user: "user"
command: "/sp.implement"
labels: ["backend", "cohere", "model", "api"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files_yaml: |
  - E:\New folder\PhysicalAIHumanoid\backend\main.py
tests_yaml: |
  - Test functionality with new model
outcome: "Updated Cohere model from command-r-plus to command-r"
evaluation: "Backend now uses supported Cohere model"
---

# Update Cohere Model to Supported Version

## User Input
```
E:\New folder\PhysicalAIHumanoid>python -m uvicorn backend.main:app --reload
←[32mINFO←[0m:     Will watch for changes in these directories: ['E:\\New folder\\PhysicalAIHumanoid']
←[32mINFO←[0m:     Uvicorn running on ←[1mhttp://127.0.0.1:8000←[0m (Press CTRL+C to quit)
←[32mINFO←[0m:     Started reloader process [←[36m←[1m6212←[0m] using ←[36m←[1mStatReload←[0m
C:\Users\ASFAR\AppData\Roaming\Python\Python314\site-packages\cohere\core\pydantic_utilities.py:13: UserWarning: Core Pydantic V1 functionality isn't compatible with Python 3.14 or greater.
  from pydantic.v1.datetime_parse import parse_date as parse_date
INFO:httpx:HTTP Request: GET https://a41eb234-d13f-4e96-a773-dcd9d5a81086.us-east4-0.gcp.cloud.qdrant.io:6333 "HTTP/1.1 200 OK"
←[32mINFO←[0m:     Started server process [←[36m11764←[0m]
←[32mINFO←[0m:     Waiting for application startup.
INFO:backend.main:Starting backend with Cohere + Qdrant
INFO:httpx:HTTP Request: GET https://a41eb234-d13f-4e96-a773-dcd9d5a81086.us-east4-0.gcp.cloud.qdrant.io:6333/collections "HTTP/1.1 200 OK"
INFO:backend.main:Qdrant collection physical_ai_docs exists
←[32mINFO←[0m:     Application startup complete.
←[32mINFO←[0m:     127.0.0.1:59773 - "←[1mOPTIONS /ask_stream HTTP/1.1←[0m" ←[32m200 OK←[0m
INFO:backend.main:Received streaming query: what is Physical AI & Humanoid Robotics
←[32mINFO←[0m:     127.0.0.1:59773 - "←[1mPOST /ask_stream HTTP/1.1←[0m" ←[32m200 OK←[0m
INFO:httpx:HTTP Request: POST https://api.cohere.com/v1/embed "HTTP/1.1 200 OK"
INFO:httpx:HTTP Request: POST https://a41eb234-d13f-4e96-a773-dcd9d5a81086.us-east4-0.gcp.cloud.qdrant.io:6333/collections/physical_ai_docs/points/scroll "HTTP/1.1 200 OK"
INFO:httpx:HTTP Request: POST https://api.cohere.com/v1/chat "HTTP/1.1 404 Not Found"
ERROR:backend.main:Cohere streaming error: headers: {'access-control-expose-headers': 'X-Debug-Trace-ID', 'cache-control': 'no-cache, no-store, no-transform, must-revalidate, private, max-age=0', 'content-encoding': 'gzip', 'content-type': 'application/json', 'expires': 'Thu, 01 Jan 1970 00:00:00 GMT', 'pragma': 'no-cache', 'vary': 'Origin,Accept-Encoding', 'x-accel-expires': '0', 'x-debug-trace-id': 'fa36dda0f7136a01b9a09348d1adb8e3', 'x-endpoint-monthly-call-limit': '1000', 'x-trial-endpoint-call-limit': '20', 'x-trial-endpoint-call-remaining': '19', 'date': 'Fri, 12 Dec 2025 10:42:31 GMT', 'x-envoy-upstream-service-time': '8', 'server': 'envoy', 'via': '1.1 google', 'alt-svc': 'h3=":443"; ma=2592000,h3-29=":443"; ma=2592000', 'transfer-encoding': 'chunked'}, status_code: 404, body: {'id': '195fdd45-b801-4b60-a637-0f76560dfd79', 'message': "model 'command-r-plus' was removed on September 15, 2025. See https://docs.cohere.com/docs/models#command for a list of models you can use instead."}
```

## Response
Updated the Cohere model from the deprecated `command-r-plus` to the supported `command-r` model in both streaming and non-streaming functions:

### Changed:
- Updated streaming function: `model="command-r-plus"` to `model="command-r"`
- Updated non-streaming function: `model="command-r-plus"` to `model="command-r"`
- The `command-r-plus` model was removed on September 15, 2025, so using `command-r` which is a currently supported model