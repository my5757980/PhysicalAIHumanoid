# Scripts for RAG Chatbot System

## Backend Management

### Start Backend Server
```bash
cd backend
python -m venv venv  # Only needed once
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt  # Only needed once
uvicorn main:app --reload --port 8000
```

### Ingest Documents
```bash
cd backend
source venv/bin/activate  # On Windows: venv\Scripts\activate
python ingest_docs.py
```

## Frontend Management

### Start Docusaurus
```bash
npm install  # Only needed once
npm start
```

## Environment Setup

### Backend .env file (backend/.env):
```
QDRANT_URL=your_qdrant_cluster_url
QDRANT_API_KEY=your_qdrant_api_key
COHERE_API_KEY=your_cohere_api_key
OPENAI_API_KEY=your_openai_api_key
```

### Frontend .env file (root/.env):
```
REACT_APP_API_BASE_URL=http://localhost:8000
```

## Complete Setup Flow

1. Create accounts and get API keys:
   - Qdrant Cloud (Free Tier)
   - Cohere
   - OpenAI

2. Set up backend:
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   # Create backend/.env with your API keys
   ```

3. Ingest documents:
   ```bash
   python ingest_docs.py
   ```

4. Start backend:
   ```bash
   uvicorn main:app --reload --port 8000
   ```

5. Set up frontend:
   ```bash
   # Create root/.env with REACT_APP_API_BASE_URL=http://localhost:8000
   npm install
   npm start
   ```

## Production Deployment Notes

1. For production, update CORS settings in backend/main.py to restrict origins
2. Consider adding authentication to the backend API endpoints
3. Set up a proper reverse proxy for the FastAPI application
4. Use a process manager like PM2 or systemd to keep the backend running