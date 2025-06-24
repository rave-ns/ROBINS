"""
Test script for the media scraper functionality
"""

import json
import requests
from scrapers import MediaScraper


def test_scraper_locally():
    """Test the scraper functionality locally"""
    print("=" * 60)
    print("TESTING MEDIA SCRAPER LOCALLY")
    print("=" * 60)
    
    scraper = MediaScraper()
    
    # Test URLs - using publicly available content
    test_urls = [
        "https://www.youtube.com/watch?v=dQw4w9WgXcQ",  # Rick Astley - Never Gonna Give You Up
        "https://youtu.be/dQw4w9WgXcQ",  # Same video, short URL
    ]
    
    for i, url in enumerate(test_urls, 1):
        print(f"\n{'-' * 40}")
        print(f"Test {i}: {url}")
        print(f"{'-' * 40}")
        
        try:
            result = scraper.scrape_media(url)
            
            if result.get('success'):
                print(f"✅ Success!")
                print(f"Platform: {result.get('platform')}")
                print(f"Title: {result.get('title', 'N/A')}")
                print(f"Duration: {result.get('duration', 'N/A')} seconds")
                print(f"Uploader: {result.get('uploader', 'N/A')}")
                print(f"Available formats: {len(result.get('formats', []))}")
                
                # Show first few formats
                formats = result.get('formats', [])[:3]
                for fmt in formats:
                    print(f"  - {fmt.get('ext', 'unknown')} | {fmt.get('quality', 'unknown')} | {fmt.get('filesize', 'unknown')} bytes")
            else:
                print(f"❌ Failed: {result.get('error')}")
                
        except Exception as e:
            print(f"❌ Exception: {str(e)}")


def test_api_endpoints():
    """Test the Flask API endpoints"""
    print("\n" + "=" * 60)
    print("TESTING FLASK API ENDPOINTS")
    print("=" * 60)
    
    base_url = "http://localhost:12000"
    api_key = "robins_secret_key_2024"
    
    # Test health endpoint
    print("\n1. Testing health endpoint...")
    try:
        response = requests.get(f"{base_url}/health")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"❌ Health check failed: {str(e)}")
    
    # Test index endpoint
    print("\n2. Testing index endpoint...")
    try:
        response = requests.get(f"{base_url}/")
        print(f"Status: {response.status_code}")
        print(f"API Info: {response.json().get('name', 'N/A')}")
    except Exception as e:
        print(f"❌ Index check failed: {str(e)}")
    
    # Test scrape endpoint without API key
    print("\n3. Testing scrape endpoint without API key...")
    try:
        response = requests.get(f"{base_url}/scrape?url=https://youtube.com/watch?v=dQw4w9WgXcQ")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"❌ No API key test failed: {str(e)}")
    
    # Test scrape endpoint with API key
    print("\n4. Testing scrape endpoint with API key...")
    try:
        headers = {'X-API-Key': api_key}
        response = requests.get(
            f"{base_url}/scrape?url=https://youtube.com/watch?v=dQw4w9WgXcQ",
            headers=headers
        )
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Success: {result.get('success')}")
            print(f"Platform: {result.get('platform')}")
            print(f"Title: {result.get('title', 'N/A')}")
        else:
            print(f"Response: {response.json()}")
    except Exception as e:
        print(f"❌ API scrape test failed: {str(e)}")


if __name__ == "__main__":
    # Test locally first
    test_scraper_locally()
    
    # Ask user if they want to test API
    print("\n" + "=" * 60)
    print("To test the API endpoints, start the Flask server first:")
    print("python app.py")
    print("Then run this script again or call test_api_endpoints() manually")
    print("=" * 60)