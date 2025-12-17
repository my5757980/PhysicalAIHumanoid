# RAG Chatbot Integration for Physical AI Humanoid Textbook

## Overview
This document provides instructions for setting up and running the RAG (Retrieval-Augmented Generation) chatbot integrated into the Physical AI & Humanoid Robotics Docusaurus textbook.

## Architecture Overview
- **Frontend**: Docusaurus 3 with React-based chat widget
- **Backend**: FastAPI server with Qdrant, Cohere, and OpenAI integration
- **Database**: Qdrant Cloud for vector storage
- **Embeddings**: Cohere multilingual embeddings
- **Generation**: OpenAI GPT for responses

## Prerequisites
- Python 3.8+
- Node.js 18+
- Qdrant Cloud account (Free Tier)
- Cohere API key
- OpenAI API key

## Setup Instructions

### 1. Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment and install dependencies:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. Create a `.env` file in the backend directory with your API keys:
```env
QDRANT_URL=your_qdrant_cluster_url
QDRANT_API_KEY=your_qdrant_api_key
COHERE_API_KEY=your_cohere_api_key
OPENAI_API_KEY=your_openai_api_key
```

4. Start the backend server:
```bash
uvicorn main:app --reload --port 8000
```

### 2. Document Ingestion

1. Before starting the chatbot, you need to ingest the textbook content:
```bash
python ingest_docs.py
```

This script will:
- Read all markdown files from the `../docs` directory
- Chunk the content (300-1200 tokens with 80-200 overlap)
- Generate embeddings using Cohere
- Store the embeddings in Qdrant

### 3. Frontend Setup

1. In the project root directory, install dependencies:
```bash
npm install
```

2. Create a `.env` file in the project root for frontend environment variables:
```env
REACT_APP_API_BASE_URL=http://localhost:8000
```

3. Start the Docusaurus development server:
```bash
npm start
```

## API Endpoints

### `/health` (GET)
Check the health status of the backend services.

### `/ask` (POST)
Ask a question to the chatbot.

Request body:
```json
{
  "query": "Your question here",
  "selected_text": "Optional selected text for priority mode",
  "max_results": 5,
  "temperature": 0.7
}
```

Response:
```json
{
  "answer": "The answer to your question",
  "sources": [...],
  "query": "Your original query",
  "timestamp": "ISO timestamp"
}
```

### `/embed` (POST)
Generate embeddings for text.

Request body:
```json
{
  "text": "Single text to embed",
  "texts": ["Multiple", "texts", "to embed"]
}
```

## Chat Widget Features

1. **Floating Chat Icon**: Appears in the bottom-right corner
2. **Text Selection Priority**: When text is selected on the page, it gets priority in the chatbot response
3. **Source Citations**: Shows which chapters/sections were used to generate the response
4. **Responsive Design**: Works on both desktop and mobile devices

## Environment Variables

### Backend (.env in backend directory)
- `QDRANT_URL`: Your Qdrant Cloud cluster URL
- `QDRANT_API_KEY`: Your Qdrant API key
- `COHERE_API_KEY`: Your Cohere API key
- `OPENAI_API_KEY`: Your OpenAI API key

### Frontend (.env in project root)
- `REACT_APP_API_BASE_URL`: URL of the backend API (default: http://localhost:8000)

## Development Tips

1. **Local Development**:
   - Backend: `uvicorn main:app --reload`
   - Frontend: `npm start`

2. **Production Deployment**:
   - Backend: Deploy the FastAPI app to a cloud provider
   - Frontend: Build with `npm run build` and serve the `build` directory

3. **Qdrant Collection**: The app automatically creates a collection named `physical_ai_docs` if it doesn't exist.

## Troubleshooting

1. **API Keys**: Ensure all API keys are correctly set in the environment files
2. **Backend Connection**: Verify the backend is running and accessible from the frontend
3. **Document Ingestion**: Make sure the `ingest_docs.py` script has run successfully before using the chatbot
4. **CORS Issues**: The backend allows all origins in development; restrict in production

## Security Considerations

1. Never commit API keys to version control
2. Use environment variables for sensitive information
3. In production, restrict CORS origins and add authentication if needed
4. Monitor API usage for cost control

## Customization

1. **Chat Widget**: Modify `src/components/ChatWidget.jsx` and `src/components/ChatWidget.css`
2. **Backend Logic**: Modify `backend/main.py` for custom behavior
3. **Chunking Strategy**: Adjust parameters in `backend/ingest_docs.py`
4. **UI Styling**: The chat widget can be customized in its CSS file