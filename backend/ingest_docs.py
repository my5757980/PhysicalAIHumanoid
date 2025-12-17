#!/usr/bin/env python3
"""
Document ingestion script for Physical AI Humanoid RAG chatbot.
This script reads Docusaurus docs, chunks them, generates embeddings, and stores them in Qdrant.
"""
from dotenv import load_dotenv
import os
load_dotenv()
import re
from pathlib import Path
from typing import List, Dict, Any, Tuple
import asyncio
import cohere
from qdrant_client import QdrantClient
from qdrant_client.http import models
import logging
from dataclasses import dataclass
import uuid  # ✅ Added for valid Qdrant IDs
import sys
# Add the parent directory to the path to import utils
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from utils import chunk_text, get_token_count, extract_section_info

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Environment variables
QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
COHERE_API_KEY = os.getenv("COHERE_API_KEY")

if not all([QDRANT_URL, QDRANT_API_KEY, COHERE_API_KEY]):
    raise ValueError("Missing required environment variables. Please set QDRANT_URL, QDRANT_API_KEY, and COHERE_API_KEY")

# Initialize clients
co = cohere.Client(COHERE_API_KEY)
qdrant_client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)

# Collection name for storing embeddings
COLLECTION_NAME = "physical_ai_book"

@dataclass
class DocumentChunk:
    id: str
    text: str
    chapter: str
    section: str
    token_count: int
    metadata: Dict[str, Any]

def read_markdown_files(docs_dir: str) -> List[Tuple[str, str, str]]:
    docs_path = Path(docs_dir)
    markdown_files = list(docs_path.rglob("*.md")) + list(docs_path.rglob("*.mdx"))

    documents = []
    for file_path in markdown_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            chapter_parts = file_path.relative_to(docs_path).parts
            chapter_name = chapter_parts[0] if len(chapter_parts) > 1 else "general"
            content = re.sub(r'^---\n.*?\n---\n', '', content, flags=re.DOTALL)
            documents.append((str(file_path), content, chapter_name))
            logger.info(f"Read file: {file_path}")
        except Exception as e:
            logger.error(f"Error reading file {file_path}: {e}")
    return documents



def generate_embeddings(texts: List[str]) -> List[List[float]]:
    if not texts:
        return []
    try:
        response = co.embed(
            texts=texts,
            model='embed-multilingual-v3.0',
            input_type="search_document"
        )
        return response.embeddings
    except Exception as e:
        logger.error(f"Error generating embeddings: {e}")
        raise


def process_documents(docs_dir: str) -> List[DocumentChunk]:
    logger.info(f"Processing documents from: {docs_dir}")
    markdown_files = read_markdown_files(docs_dir)
    all_chunks = []

    for file_path, content, chapter_name in markdown_files:
        logger.info(f"Processing: {file_path}")
        section_info = extract_section_info(content)
        chunks = chunk_text(content, max_tokens=800, overlap_tokens=150)
        for i, chunk in enumerate(chunks):
            token_count = get_token_count(chunk)
            # ✅ Use UUID for valid Qdrant ID
            doc_chunk = DocumentChunk(
                id=str(uuid.uuid4()),
                text=chunk,
                chapter=chapter_name,
                section=section_info,
                token_count=token_count,
                metadata={
                    "file_path": file_path,
                    "chunk_index": i,
                    "total_chunks": len(chunks),
                    "source_file": os.path.basename(file_path)
                }
            )
            all_chunks.append(doc_chunk)
            logger.debug(f"Created chunk {i+1}/{len(chunks)} for {file_path} ({token_count} tokens)")

    logger.info(f"Total chunks created: {len(all_chunks)}")
    return all_chunks

def store_in_qdrant(chunks: List[DocumentChunk], batch_size: int = 10):
    logger.info(f"Storing {len(chunks)} chunks in Qdrant collection: {COLLECTION_NAME}")

    try:
        collections = qdrant_client.get_collections()
        collection_exists = any(collection.name == COLLECTION_NAME for collection in collections.collections)

        if not collection_exists:
            qdrant_client.create_collection(
                collection_name=COLLECTION_NAME,
                vectors_config=models.VectorParams(size=1024, distance=models.Distance.COSINE),
            )
            logger.info(f"Created Qdrant collection: {COLLECTION_NAME}")
        else:
            logger.info(f"Qdrant collection {COLLECTION_NAME} already exists")
    except Exception as e:
        logger.error(f"Error checking/creating collection: {e}")
        raise

    for i in range(0, len(chunks), batch_size):
        batch_chunks = chunks[i:i + batch_size]
        texts = [chunk.text for chunk in batch_chunks]

        try:
            embeddings = generate_embeddings(texts)
            points = []
            for chunk, embedding in zip(batch_chunks, embeddings):
                point = models.PointStruct(
                    id=chunk.id,  # ✅ Already UUID
                    vector=embedding,
                    payload={
                        "text": chunk.text,
                        "chapter": chunk.chapter,
                        "section": chunk.section,
                        "token_count": chunk.token_count,
                        "metadata": chunk.metadata
                    }
                )
                points.append(point)

            qdrant_client.upsert(
                collection_name=COLLECTION_NAME,
                points=points,
                wait=True
            )
            logger.info(f"Uploaded batch {i//batch_size + 1}: {len(points)} points")

        except Exception as e:
            logger.error(f"Error processing batch {i//batch_size + 1}: {e}")
            raise

    logger.info(f"Successfully stored {len(chunks)} chunks in Qdrant")

def main():
    docs_dir = "../docs"
    if not os.path.exists(docs_dir):
        docs_dir = "docs"
        if not os.path.exists(docs_dir):
            raise FileNotFoundError(f"Docs directory not found at {docs_dir}")

    logger.info("Starting document ingestion process...")

    try:
        chunks = process_documents(docs_dir)
        if not chunks:
            logger.warning("No chunks were created. Check if docs directory contains markdown files.")
            return
        store_in_qdrant(chunks)
        logger.info("Document ingestion completed successfully!")
        logger.info(f"Total documents processed: {len(chunks)}")
    except Exception as e:
        logger.error(f"Document ingestion failed: {e}")
        raise

if __name__ == "__main__":
    main()
