from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from fastapi.responses import StreamingResponse
import json
import os
import logging
from contextlib import asynccontextmanager
import cohere
from qdrant_client import QdrantClient
from qdrant_client.http import models
from datetime import datetime
from dotenv import load_dotenv
from pathlib import Path

# Load .env
env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Environment variables
QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
COHERE_API_KEY = os.getenv("COHERE_API_KEY")

if not all([QDRANT_URL, QDRANT_API_KEY, COHERE_API_KEY]):
    logger.warning("Missing required environment variables. Set QDRANT_URL, QDRANT_API_KEY, COHERE_API_KEY.")

# Initialize clients
co = cohere.Client(COHERE_API_KEY) if COHERE_API_KEY else None
qdrant_client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY) if QDRANT_URL and QDRANT_API_KEY else None

# Collection name
COLLECTION_NAME = "physical_ai_book"

# Models
class QueryRequest(BaseModel):
    query: str
    selected_text: Optional[str] = None
    max_results: Optional[int] = 5
    temperature: Optional[float] = 0.7

class QueryResponse(BaseModel):
    answer: str
    sources: List[Dict[str, Any]]
    query: str
    timestamp: str
    validation: Optional[Dict[str, Any]] = None  # For hallucination detection results

class EmbedRequest(BaseModel):
    text: str
    texts: Optional[List[str]] = None

class EmbedResponse(BaseModel):
    embeddings: List[List[float]]
    text: Optional[str] = None
    texts: Optional[List[str]] = None

class HealthResponse(BaseModel):
    status: str
    timestamp: str
    services: Dict[str, bool]

# Lifespan
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting backend with Cohere + Qdrant")
    # Ensure collection exists
    if qdrant_client:
        try:
            collections = qdrant_client.get_collections()
            exists = any(c.name == COLLECTION_NAME for c in collections.collections)
            if not exists:
                qdrant_client.create_collection(
                    collection_name=COLLECTION_NAME,
                    vectors_config=models.VectorParams(size=1024, distance=models.Distance.COSINE)
                )
                logger.info(f"Created Qdrant collection: {COLLECTION_NAME}")
            else:
                logger.info(f"Qdrant collection {COLLECTION_NAME} exists")
        except Exception as e:
            logger.error(f"Qdrant init error: {e}")
    yield
    logger.info("Shutting down backend")

# FastAPI app
app = FastAPI(title="Physical AI Humanoid RAG Chatbot API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Functions
def get_embeddings(texts: List[str]) -> List[List[float]]:
    if not co:
        raise HTTPException(status_code=500, detail="Cohere client not initialized")
    try:
        response = co.embed(
            texts=texts,
            model="embed-english-v3.0",
            input_type="search_document"
        )
        return response.embeddings
    except Exception as e:
        logger.error(f"Cohere embedding error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

def search_documents(query: str, max_results: int = 5) -> List[Dict[str, Any]]:
    if not qdrant_client:
        raise HTTPException(status_code=500, detail="Qdrant client not initialized")
    try:
        query_embedding = get_embeddings([query])[0]
        # Use scroll-based similarity search as primary method for compatibility
        # Retrieve all points from the collection
        records, _ = qdrant_client.scroll(
            collection_name=COLLECTION_NAME,
            limit=1000,  # Adjust as needed
            with_payload=True,
            with_vectors=True
        )

        # Simple similarity search using cosine similarity
        import numpy as np
        query_vec = np.array(query_embedding)

        scored_results = []
        for record in records:
            doc_vec = np.array(record.vector)
            # Calculate cosine similarity
            cosine_sim = np.dot(query_vec, doc_vec) / (np.linalg.norm(query_vec) * np.linalg.norm(doc_vec))

            scored_results.append({
                "id": record.id,
                "text": record.payload.get("text", ""),
                "chapter": record.payload.get("chapter", ""),
                "section": record.payload.get("section", ""),
                "score": float(cosine_sim),
                "metadata": record.payload.get("metadata", {})
            })

        # Sort by score in descending order and return top results
        scored_results.sort(key=lambda x: x["score"], reverse=True)
        return scored_results[:max_results]
    except Exception as e:
        logger.error(f"Qdrant search error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

def create_context_summary(query: str, context: str, sources: List[Dict[str, Any]]) -> str:
    """
    Create a structured summary from the context when OpenAI is not available.
    This provides a more useful response than just raw context.
    """
    # Create a more structured response
    summary_parts = [
        f"Based on the Physical AI & Humanoid Robotics textbook, here's information related to your query: '{query}'",
        "",
        "Relevant content from the textbook:",
        ""
    ]

    # Add snippets from the most relevant sources
    for i, source in enumerate(sources[:3]):  # Limit to top 3 sources
        section_info = source.get('section', 'Unknown Section')
        chapter_info = source.get('chapter', 'Unknown Chapter')
        relevance_score = source.get('relevance_score', 0)

        summary_parts.append(f"From {chapter_info} - {section_info} (relevance: {relevance_score:.2f}):")
        text_snippet = source['text'][:500] + "..." if len(source['text']) > 500 else source['text']
        summary_parts.append(f"{text_snippet}")
        summary_parts.append("")  # Add blank line between sources

    return "\n".join(summary_parts)

def detect_hallucination(answer: str, context: str, sources: List[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Enhanced hallucination detection by checking if the answer is supported by the context
    and validating citation accuracy.
    This is a simplified implementation - a production system would use more sophisticated NLP techniques.
    """
    import re

    # Convert both to lowercase for comparison
    answer_lower = answer.lower()
    context_lower = context.lower()

    # Extract key phrases from the answer that should appear in the context
    # This is a basic check - look for specific technical terms or concepts
    key_terms = re.findall(r'\b(?:physical ai|humanoid|robotics|kinematics|dynamics|control|embodiment|perception|learning|actuators|sensors|locomotion|manipulation|slam|reinforcement learning|imitation learning)\b', answer_lower)

    # Count how many key terms are found in the context
    matched_terms = [term for term in key_terms if term in context_lower]

    # Calculate a basic confidence score
    confidence_score = len(matched_terms) / len(key_terms) if key_terms else 1.0

    # Check if the answer contains phrases indicating uncertainty (which might indicate hallucination was avoided)
    uncertainty_phrases = ["i don't know", "not mentioned", "not specified", "not found", "not in the text"]
    has_uncertainty = any(phrase in answer_lower for phrase in uncertainty_phrases)

    # Check citation accuracy if sources are provided
    citation_accuracy = 1.0  # Default to perfect accuracy
    citation_issues = []

    if sources:
        # Check if the answer references content that's actually in the provided sources
        source_texts = [source['text'].lower() for source in sources]
        source_full_text = " ".join(source_texts)

        # Check if key terms from the answer appear in the sources
        source_matched_terms = [term for term in key_terms if term in source_full_text]
        citation_accuracy = len(source_matched_terms) / len(key_terms) if key_terms else 1.0

        # Identify any discrepancies
        if len(source_matched_terms) < len(matched_terms):
            citation_issues.append("Some concepts in the answer may not be fully supported by the provided sources")

    # Check if answer seems to make claims not supported by context
    has_hallucination = confidence_score < 0.3 and not has_uncertainty  # Basic threshold
    has_citation_issues = citation_accuracy < 0.5

    return {
        "has_hallucination": has_hallucination,
        "has_citation_issues": has_citation_issues,
        "confidence_score": confidence_score,
        "citation_accuracy": citation_accuracy,
        "matched_terms": matched_terms,
        "total_terms": len(key_terms),
        "citation_issues": citation_issues,
        "has_uncertainty_indicators": has_uncertainty,
        "message": f"Answer validation: {confidence_score:.2%} of key terms found in context, citation accuracy: {citation_accuracy:.2%}" if not has_hallucination and not has_citation_issues else "Potential issues detected: low confidence in context support or citation accuracy"
    }

# Endpoints
@app.post("/ask", response_model=QueryResponse)
async def ask_question(request: QueryRequest):
    logger.info(f"Received query: {request.query}")
    try:
        search_results = search_documents(request.query, request.max_results)
        context_parts = [res["text"] for res in search_results]
        sources = [{"id": r["id"], "text": r["text"][:200]+"..." if len(r["text"])>200 else r["text"],
                    "chapter": r["chapter"], "section": r["section"], "relevance_score": r["score"]} for r in search_results]
        context = "\n\n".join(context_parts)

        # Use Cohere to generate a proper answer based on the context
        if co:
            try:
                # Create a prompt that includes the query and the retrieved context
                final_prompt = f"""Based on the following context from the Physical AI & Humanoid Robotics textbook, please answer the user's question. If the context doesn't contain the information needed to answer the question, please say so clearly.

Context:
{context}

User's question: {request.query}

Please provide a clear, concise answer based on the context, and cite relevant sections when possible."""

                response = co.chat(
                    model="command-r-08-2024",
                    message=final_prompt,
                    temperature=request.temperature
                )

                answer = response.text

                # Perform hallucination detection with source validation
                validation_result = detect_hallucination(answer, context, sources)
            except Exception as e:
                logger.error(f"Cohere error: {e}")
                # Fallback to structured context summary if Cohere fails
                answer = create_context_summary(request.query, context, sources)
        else:
            # Fallback if Cohere is not configured
            answer = create_context_summary(request.query, context, sources)
            # Perform hallucination detection on the fallback answer as well
            validation_result = detect_hallucination(answer, context, sources)

        # Add validation result if Cohere was used and validation was performed
        validation = validation_result if 'validation_result' in locals() else None
        return QueryResponse(answer=answer, sources=sources, query=request.query, timestamp=datetime.now().isoformat(), validation=validation)
    except Exception as e:
        logger.error(f"Error processing query: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/ask_stream", response_class=StreamingResponse)
async def ask_stream(request: QueryRequest):
    logger.info(f"Received streaming query: {request.query}")

    async def generate_stream():
        try:
            search_results = search_documents(request.query, request.max_results)
            context_parts = [res["text"] for res in search_results]
            sources = [{"id": r["id"], "text": r["text"][:200]+"..." if len(r["text"])>200 else r["text"],
                        "chapter": r["chapter"], "section": r["section"], "relevance_score": r["score"]} for r in search_results]
            context = "\n\n".join(context_parts)

            # Stream the sources first
            sources_data = {
                "type": "sources",
                "sources": sources,
                "query": request.query
            }
            yield f"data: {json.dumps(sources_data)}\n\n"

            # Use Cohere to generate a proper answer based on the context with streaming
            if co:
                try:
                    # Create a prompt that includes the query and the retrieved context
                    final_prompt = f"""Based on the following context from the Physical AI & Humanoid Robotics textbook, please answer the user's question. If the context doesn't contain the information needed to answer the question, please say so clearly.

Context:
{context}

User's question: {request.query}

Please provide a clear, concise answer based on the context, and cite relevant sections when possible."""

                    response = co.chat_stream(
                        model="command-r-08-2024",
                        message=final_prompt
                    )

                    # Stream the response chunks
                    full_answer = ""
                    for event in response:
                        if hasattr(event, 'text') and event.text:
                            content = event.text
                            full_answer += content

                            # Yield each chunk as it arrives
                            chunk_data = {
                                "type": "answer_chunk",
                                "content": content
                            }
                            yield f"data: {json.dumps(chunk_data)}\n\n"

                    # Perform hallucination detection on the complete answer with source validation
                    validation_result = detect_hallucination(full_answer, context, sources)

                    # Send completion message with validation
                    completion_data = {
                        "type": "completion",
                        "answer": full_answer,
                        "validation": validation_result
                    }
                    yield f"data: {json.dumps(completion_data)}\n\n"

                except Exception as e:
                    logger.error(f"Cohere streaming error: {e}")
                    # Fallback to structured context summary if Cohere fails
                    fallback_answer = create_context_summary(request.query, context, sources)

                    # Perform hallucination detection on the fallback answer
                    validation_result = detect_hallucination(fallback_answer, context, sources)

                    # Send completion message with fallback answer
                    completion_data = {
                        "type": "completion",
                        "answer": fallback_answer,
                        "validation": validation_result
                    }
                    yield f"data: {json.dumps(completion_data)}\n\n"
            else:
                # Fallback if Cohere is not configured
                fallback_answer = create_context_summary(request.query, context, sources)

                # Perform hallucination detection on the fallback answer
                validation_result = detect_hallucination(fallback_answer, context, sources)

                # Send completion message with fallback answer
                completion_data = {
                    "type": "completion",
                    "answer": fallback_answer,
                    "validation": validation_result
                }
                yield f"data: {json.dumps(completion_data)}\n\n"

        except Exception as e:
            logger.error(f"Error processing streaming query: {e}")
            error_data = {
                "type": "error",
                "message": str(e)
            }
            yield f"data: {json.dumps(error_data)}\n\n"

    return StreamingResponse(generate_stream(), media_type="text/plain")

@app.post("/embed", response_model=EmbedResponse)
async def generate_embeddings(request: EmbedRequest):
    texts_to_embed = [request.text] if request.text else []
    if request.texts:
        texts_to_embed.extend(request.texts)
    if not texts_to_embed:
        raise HTTPException(status_code=400, detail="Provide text or texts")
    embeddings = get_embeddings(texts_to_embed)
    return EmbedResponse(embeddings=embeddings, text=request.text, texts=request.texts)

@app.get("/health", response_model=HealthResponse)
async def health_check():
    services_status = {
        "cohere": co is not None,
        "qdrant": qdrant_client is not None
    }
    overall_status = "healthy" if all(services_status.values()) else "degraded"
    return HealthResponse(status=overall_status, timestamp=datetime.now().isoformat(), services=services_status)

@app.get("/")
async def root():
    return {"message": "Physical AI Humanoid RAG Chatbot API", "status": "running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
