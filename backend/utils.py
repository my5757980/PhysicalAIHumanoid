"""
Utility functions for the Physical AI Humanoid RAG Chatbot
Contains chunking, embedding, and retrieval functions
"""
import re
from typing import List, Dict, Any
import logging
import numpy as np

logger = logging.getLogger(__name__)

def chunk_text(text: str, max_tokens: int = 1000, overlap_tokens: int = 150) -> List[str]:
    """
    Split text into chunks with specified maximum token count and overlap
    """
    sentences = re.split(r'(?<=[.!?])\s+', text)
    chunks = []
    current_chunk = ""
    current_token_count = 0

    for sentence in sentences:
        sentence_tokens = len(sentence.split())
        if current_token_count + sentence_tokens > max_tokens and current_chunk:
            chunks.append(current_chunk.strip())
            if overlap_tokens > 0:
                words = current_chunk.split()
                overlap_start = max(0, len(words) - overlap_tokens)
                current_chunk = " ".join(words[overlap_start:])
                current_token_count = len(words[overlap_start:])
            else:
                current_chunk = ""
                current_token_count = 0

        current_chunk += " " + sentence if current_chunk else sentence
        current_token_count += sentence_tokens

    if current_chunk.strip():
        chunks.append(current_chunk.strip())

    # Filter out very small chunks
    chunks = [chunk for chunk in chunks if len(chunk.split()) > 20]
    return chunks

def get_token_count(text: str) -> int:
    """
    Simple token count estimation using word splitting
    """
    return len(text.split())

def cosine_similarity(vec1: List[float], vec2: List[float]) -> float:
    """
    Calculate cosine similarity between two vectors
    """
    v1 = np.array(vec1)
    v2 = np.array(vec2)
    return float(np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2)))

def extract_section_info(content: str, max_context_length: int = 200) -> str:
    """
    Extract section information from content (headers or first part)
    """
    headers = re.findall(r'^(#+\s+.*?)(?=\n#|\n\n|$)', content, re.MULTILINE)
    if headers:
        return headers[0].strip()
    return content[:max_context_length].strip() + "..." if len(content) > max_context_length else content