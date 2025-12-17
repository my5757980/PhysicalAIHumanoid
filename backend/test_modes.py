"""
Test script for validating text-selection mode and normal mode functionality
"""
import requests
import time
import json
from typing import Dict, Any

def test_normal_mode(api_base_url: str):
    """Test normal mode (without selected text)"""
    print("Testing normal mode functionality...")

    test_payload = {
        "query": "What is Physical AI?",
        "selected_text": None,
        "max_results": 5,
        "temperature": 0.7
    }

    try:
        response = requests.post(f"{api_base_url}/ask", json=test_payload)
        if response.status_code == 200:
            data = response.json()
            print(f"✓ Normal mode query successful")
            print(f"  Answer preview: {data['answer'][:100]}...")
            print(f"  Sources returned: {len(data['sources'])}")
            if 'validation' in data and data['validation']:
                print(f"  Validation: {data['validation']['message']}")
            return True
        else:
            print(f"✗ Normal mode query failed with status {response.status_code}")
            print(f"  Response: {response.text}")
            return False
    except Exception as e:
        print(f"✗ Normal mode test error: {e}")
        return False

def test_text_selection_mode(api_base_url: str):
    """Test text-selection mode (with selected text)"""
    print("\nTesting text-selection mode functionality...")

    # Example selected text about Physical AI
    selected_text = "Physical AI is an emerging field that combines artificial intelligence with physical systems. Unlike traditional AI that operates in digital spaces, Physical AI involves embodied intelligence that interacts with the physical world through sensors, actuators, and control systems."

    test_payload = {
        "query": "Explain the concept mentioned in the selected text",
        "selected_text": selected_text,
        "max_results": 5,
        "temperature": 0.7
    }

    try:
        response = requests.post(f"{api_base_url}/ask", json=test_payload)
        if response.status_code == 200:
            data = response.json()
            print(f"✓ Text-selection mode query successful")
            print(f"  Answer preview: {data['answer'][:100]}...")
            print(f"  Sources returned: {len(data['sources'])}")
            if 'validation' in data and data['validation']:
                print(f"  Validation: {data['validation']['message']}")
            return True
        else:
            print(f"✗ Text-selection mode query failed with status {response.status_code}")
            print(f"  Response: {response.text}")
            return False
    except Exception as e:
        print(f"✗ Text-selection mode test error: {e}")
        return False

def test_streaming_functionality(api_base_url: str):
    """Test streaming functionality"""
    print("\nTesting streaming functionality...")

    test_payload = {
        "query": "What are the core components of Physical AI?",
        "selected_text": None,
        "max_results": 5,
        "temperature": 0.7
    }

    try:
        response = requests.post(f"{api_base_url}/ask_stream", json=test_payload, stream=True)
        if response.status_code == 200:
            print("✓ Streaming connection established")

            # Process streaming response
            full_answer = ""
            sources_received = False
            answer_chunks_received = 0

            for line in response.iter_lines():
                if line:
                    line_str = line.decode('utf-8')
                    if line_str.startswith("data: "):
                        try:
                            data = json.loads(line_str[6:])  # Remove "data: " prefix
                            if data['type'] == 'sources':
                                sources_received = True
                                print(f"  Sources received: {len(data['sources'])}")
                            elif data['type'] == 'answer_chunk':
                                answer_chunks_received += 1
                                full_answer += data['content']
                            elif data['type'] == 'completion':
                                print(f"  Streaming completed, total chunks: {answer_chunks_received}")
                                print(f"  Final answer preview: {data['answer'][:100]}...")
                                if 'validation' in data and data['validation']:
                                    print(f"  Validation: {data['validation']['message']}")
                        except json.JSONDecodeError:
                            continue

            print("✓ Streaming functionality test completed")
            return True
        else:
            print(f"✗ Streaming test failed with status {response.status_code}")
            print(f"  Response: {response.text}")
            return False
    except Exception as e:
        print(f"✗ Streaming test error: {e}")
        return False

def test_health_check(api_base_url: str):
    """Test health check endpoint"""
    print("\nTesting health check functionality...")

    try:
        response = requests.get(f"{api_base_url}/health")
        if response.status_code == 200:
            data = response.json()
            print(f"✓ Health check successful")
            print(f"  Status: {data['status']}")
            print(f"  Services: {data['services']}")
            return True
        else:
            print(f"✗ Health check failed with status {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Health check test error: {e}")
        return False

def main():
    """Main test function"""
    print("Starting text-selection and normal mode functionality tests...\n")

    # Use the default API URL, but allow override
    api_base_url = "http://localhost:8000"

    print(f"Testing against API: {api_base_url}")

    # Run all tests
    results = []

    results.append(test_health_check(api_base_url))
    results.append(test_normal_mode(api_base_url))
    results.append(test_text_selection_mode(api_base_url))
    results.append(test_streaming_functionality(api_base_url))

    # Summary
    passed = sum(results)
    total = len(results)

    print(f"\nTest Results Summary:")
    print(f"Passed: {passed}/{total}")

    if passed == total:
        print("✓ All functionality tests passed!")
        return True
    else:
        print(f"✗ {total - passed} tests failed.")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)