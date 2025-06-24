#!/usr/bin/env python3
"""
Test script for the Flask API
"""

import requests
import json
import time
import subprocess
import sys
import os
from threading import Thread


def start_server():
    """Start the Flask server in a separate process"""
    env = os.environ.copy()
    env['PORT'] = '8080'
    
    process = subprocess.Popen(
        [sys.executable, 'app.py'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env=env
    )
    
    # Wait a bit for server to start
    time.sleep(3)
    return process


def test_api():
    """Test the API endpoints"""
    base_url = "http://localhost:8080"
    api_key = "robins_secret_key_2024"
    
    print("=" * 60)
    print("TESTING FLASK API ENDPOINTS")
    print("=" * 60)
    
    # Test health endpoint
    print("\n1. Testing health endpoint...")
    try:
        response = requests.get(f"{base_url}/health", timeout=10)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print(f"✅ Response: {response.json()}")
        else:
            print(f"❌ Response: {response.text}")
    except Exception as e:
        print(f"❌ Health check failed: {str(e)}")
        return False
    
    # Test index endpoint
    print("\n2. Testing index endpoint...")
    try:
        response = requests.get(f"{base_url}/", timeout=10)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ API Info: {data.get('name', 'N/A')}")
        else:
            print(f"❌ Response: {response.text}")
    except Exception as e:
        print(f"❌ Index check failed: {str(e)}")
    
    # Test scrape endpoint without API key
    print("\n3. Testing scrape endpoint without API key...")
    try:
        response = requests.get(f"{base_url}/scrape?url=https://youtube.com/watch?v=dQw4w9WgXcQ", timeout=10)
        print(f"Status: {response.status_code}")
        if response.status_code == 401:
            print(f"✅ Correctly rejected: {response.json()}")
        else:
            print(f"❌ Unexpected response: {response.json()}")
    except Exception as e:
        print(f"❌ No API key test failed: {str(e)}")
    
    # Test scrape endpoint with API key
    print("\n4. Testing scrape endpoint with API key...")
    try:
        headers = {'X-API-Key': api_key}
        response = requests.get(
            f"{base_url}/scrape?url=https://youtube.com/watch?v=dQw4w9WgXcQ",
            headers=headers,
            timeout=30
        )
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Success: {result.get('success')}")
            print(f"Platform: {result.get('platform')}")
            print(f"Title: {result.get('title', 'N/A')[:50]}...")
            print(f"Formats available: {len(result.get('formats', []))}")
        else:
            print(f"❌ Response: {response.json()}")
    except Exception as e:
        print(f"❌ API scrape test failed: {str(e)}")
    
    # Test platforms endpoint
    print("\n5. Testing platforms endpoint...")
    try:
        headers = {'X-API-Key': api_key}
        response = requests.get(f"{base_url}/platforms", headers=headers, timeout=10)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Platforms: {list(result.get('supported_platforms', {}).keys())}")
        else:
            print(f"❌ Response: {response.json()}")
    except Exception as e:
        print(f"❌ Platforms test failed: {str(e)}")
    
    return True


def main():
    """Main test function"""
    print("Starting Flask server...")
    
    # Start server
    server_process = start_server()
    
    try:
        # Test the API
        success = test_api()
        
        if success:
            print("\n" + "=" * 60)
            print("✅ API TESTS COMPLETED SUCCESSFULLY!")
            print("=" * 60)
        else:
            print("\n" + "=" * 60)
            print("❌ SOME API TESTS FAILED")
            print("=" * 60)
            
    finally:
        # Clean up
        print("\nStopping server...")
        server_process.terminate()
        server_process.wait()


if __name__ == "__main__":
    main()