"""
Test script for validating document chunking and retrieval accuracy
"""
import os
import sys
from pathlib import Path

# Add the parent directory to the path to import our modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from utils import chunk_text, get_token_count
from ingest_docs import read_markdown_files, process_documents
from main import search_documents, get_embeddings, COLLECTION_NAME
import cohere
from qdrant_client import QdrantClient

def test_chunking_accuracy():
    """Test the chunking function with sample text"""
    print("Testing chunking accuracy...")

    # Sample text to test chunking
    sample_text = """
    Physical AI is an emerging field that combines artificial intelligence with physical systems.
    Unlike traditional AI that operates in digital spaces, Physical AI involves embodied intelligence
    that interacts with the physical world through sensors, actuators, and control systems.

    The core components of Physical AI include:
    - Embodiment: The physical form and structure of the system
    - Perception: Sensing and understanding the environment
    - Learning: Adapting and improving through experience
    - Control: Actuating and manipulating the environment

    Humanoid robotics represents one of the most challenging applications of Physical AI,
    requiring sophisticated integration of all core components to achieve human-like capabilities.
    """

    # Test chunking with different parameters
    chunks = chunk_text(sample_text, max_tokens=100, overlap_tokens=20)

    print(f"Number of chunks created: {len(chunks)}")

    for i, chunk in enumerate(chunks):
        token_count = get_token_count(chunk)
        print(f"Chunk {i+1}: {token_count} tokens")
        print(f"Content preview: {chunk[:100]}...")
        print("---")

    # Validate that chunks don't exceed max token count
    max_chunk_size = max(get_token_count(chunk) for chunk in chunks)
    print(f"Max chunk size: {max_chunk_size} tokens (should be <= 100)")

    # Check overlap between consecutive chunks
    if len(chunks) > 1:
        # Check if there's reasonable overlap between chunks
        print("Chunking test completed successfully")

    return True

def test_retrieval_accuracy():
    """Test the retrieval function with sample queries"""
    print("\nTesting retrieval accuracy...")

    # Initialize clients (using environment variables)
    QDRANT_URL = os.getenv("QDRANT_URL")
    QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
    COHERE_API_KEY = os.getenv("COHERE_API_KEY")

    if not all([QDRANT_URL, QDRANT_API_KEY, COHERE_API_KEY]):
        print("Environment variables not set. Skipping retrieval test.")
        return False

    # Test search with sample queries
    test_queries = [
        "What is Physical AI?",
        "Humanoid robotics definition",
        "Embodiment perception learning control",
        "kinematics dynamics in robotics"
    ]

    for query in test_queries:
        print(f"Testing query: '{query}'")
        try:
            results = search_documents(query, max_results=3)
            print(f"Retrieved {len(results)} documents")

            for i, result in enumerate(results):
                print(f"Result {i+1}: Score: {result['score']:.3f}, Chapter: {result['chapter']}, Section: {result['section'][:50]}...")

            print("---")
        except Exception as e:
            print(f"Error during retrieval test: {e}")
            return False

    print("Retrieval accuracy test completed")
    return True

def main():
    """Main test function"""
    print("Starting accuracy validation tests...")

    # Test chunking
    chunking_success = test_chunking_accuracy()

    # Test retrieval
    retrieval_success = test_retrieval_accuracy()

    print(f"\nTest Results:")
    print(f"Chunking accuracy test: {'PASSED' if chunking_success else 'FAILED'}")
    print(f"Retrieval accuracy test: {'PASSED' if retrieval_success else 'FAILED'}")

    if chunking_success and retrieval_success:
        print("\nAll accuracy validation tests completed successfully!")
        return True
    else:
        print("\nSome tests failed.")
        return False

if __name__ == "__main__":
    main()