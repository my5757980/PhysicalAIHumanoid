@echo off
echo Starting Physical AI RAG Backend...
cd /d "%~dp0backend"
python -m uvicorn main:app --port 8001 --host 127.0.0.1
