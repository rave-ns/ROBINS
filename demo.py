#!/usr/bin/env python3
"""
Demonstration script for the Media Scraper functionality
"""

import json
from scrapers import MediaScraper


def demo_scraper():
    """Demonstrate the scraper functionality"""
    print("=" * 80)
    print("ROBINS MEDIA SCRAPER DEMONSTRATION")
    print("=" * 80)
    
    scraper = MediaScraper()
    
    # Test URLs
    test_urls = [
        "https://www.youtube.com/watch?v=dQw4w9WgXcQ",  # Rick Roll
        "https://youtu.be/dQw4w9WgXcQ",  # Same video, short URL
    ]
    
    for i, url in enumerate(test_urls, 1):
        print(f"\n{'-' * 60}")
        print(f"Test {i}: Scraping {url}")
        print(f"{'-' * 60}")
        
        try:
            result = scraper.scrape_media(url)
            
            if result.get('success'):
                print(f"✅ SUCCESS!")
                print(f"Platform: {result.get('platform', 'Unknown')}")
                print(f"Title: {result.get('title', 'N/A')}")
                print(f"Duration: {result.get('duration', 'N/A')} seconds")
                print(f"Uploader: {result.get('uploader', 'N/A')}")
                print(f"Upload Date: {result.get('upload_date', 'N/A')}")
                print(f"View Count: {result.get('view_count', 'N/A'):,}" if result.get('view_count') else "View Count: N/A")
                print(f"Thumbnail: {result.get('thumbnail', 'N/A')}")
                
                formats = result.get('formats', [])
                print(f"\nAvailable Formats: {len(formats)}")
                
                # Group formats by type
                video_formats = [f for f in formats if f.get('vcodec') != 'none' and f.get('ext') not in ['mhtml']]
                audio_formats = [f for f in formats if f.get('acodec') != 'none' and f.get('vcodec') == 'none']
                other_formats = [f for f in formats if f not in video_formats and f not in audio_formats]
                
                if video_formats:
                    print(f"\n📹 Video Formats ({len(video_formats)}):")
                    for fmt in video_formats[:5]:  # Show first 5
                        size_info = f"{fmt.get('filesize', 'Unknown')} bytes" if fmt.get('filesize') else "Size unknown"
                        resolution = f"{fmt.get('width', '?')}x{fmt.get('height', '?')}" if fmt.get('width') else "Resolution unknown"
                        print(f"  - {fmt.get('ext', 'unknown')} | {fmt.get('quality', 'unknown')} | {resolution} | {size_info}")
                
                if audio_formats:
                    print(f"\n🎵 Audio Formats ({len(audio_formats)}):")
                    for fmt in audio_formats[:5]:  # Show first 5
                        size_info = f"{fmt.get('filesize', 'Unknown')} bytes" if fmt.get('filesize') else "Size unknown"
                        print(f"  - {fmt.get('ext', 'unknown')} | {fmt.get('quality', 'unknown')} | {size_info}")
                
                if other_formats:
                    print(f"\n📄 Other Formats ({len(other_formats)}):")
                    for fmt in other_formats[:3]:  # Show first 3
                        print(f"  - {fmt.get('ext', 'unknown')} | {fmt.get('quality', 'unknown')}")
                
                # Show sample download URL (first video format if available)
                if video_formats:
                    sample_url = video_formats[0].get('url', 'N/A')
                    print(f"\n🔗 Sample Download URL:")
                    print(f"  {sample_url[:100]}..." if len(sample_url) > 100 else f"  {sample_url}")
                
            else:
                print(f"❌ FAILED: {result.get('error', 'Unknown error')}")
                
        except Exception as e:
            print(f"❌ EXCEPTION: {str(e)}")
    
    print(f"\n{'-' * 60}")
    print("PLATFORM IDENTIFICATION DEMO")
    print(f"{'-' * 60}")
    
    test_platform_urls = [
        "https://www.youtube.com/watch?v=example",
        "https://youtu.be/example",
        "https://www.tiktok.com/@user/video/123456789",
        "https://www.instagram.com/p/example/",
        "https://twitter.com/user/status/123456789",
        "https://x.com/user/status/123456789",
        "https://example.com/video",
    ]
    
    for url in test_platform_urls:
        platform = scraper.identify_platform(url)
        print(f"  {url:<50} -> {platform}")


def demo_api_structure():
    """Demonstrate the API response structure"""
    print(f"\n{'-' * 60}")
    print("API RESPONSE STRUCTURE DEMO")
    print(f"{'-' * 60}")
    
    sample_response = {
        "success": True,
        "platform": "youtube",
        "title": "Rick Astley - Never Gonna Give You Up (Official Video)",
        "description": "The official video for 'Never Gonna Give You Up' by Rick Astley...",
        "duration": 213,
        "thumbnail": "https://i.ytimg.com/vi/dQw4w9WgXcQ/maxresdefault.jpg",
        "uploader": "Rick Astley",
        "upload_date": "20091025",
        "view_count": 1667757378,
        "like_count": None,
        "formats": [
            {
                "format_id": "22",
                "ext": "mp4",
                "quality": "720p",
                "filesize": 50000000,
                "url": "https://example.com/download/video.mp4",
                "vcodec": "avc1.64001F",
                "acodec": "mp4a.40.2",
                "width": 1280,
                "height": 720,
                "fps": 30,
                "tbr": 1000
            },
            {
                "format_id": "140",
                "ext": "m4a",
                "quality": "medium",
                "filesize": 3500000,
                "url": "https://example.com/download/audio.m4a",
                "vcodec": "none",
                "acodec": "mp4a.40.2",
                "width": None,
                "height": None,
                "fps": None,
                "tbr": 128
            }
        ],
        "total_formats": 2,
        "scraped_url": "https://youtube.com/watch?v=dQw4w9WgXcQ",
        "filters_applied": {
            "format": None,
            "quality": None
        }
    }
    
    print("Sample API Response:")
    print(json.dumps(sample_response, indent=2))


def demo_api_usage():
    """Demonstrate API usage examples"""
    print(f"\n{'-' * 60}")
    print("API USAGE EXAMPLES")
    print(f"{'-' * 60}")
    
    examples = [
        {
            "title": "Basic scraping request",
            "method": "GET",
            "url": "/scrape?url=https://youtube.com/watch?v=dQw4w9WgXcQ",
            "headers": {"X-API-Key": "your_api_key"},
            "description": "Scrape all available formats from a YouTube video"
        },
        {
            "title": "Filter by format",
            "method": "GET", 
            "url": "/scrape?url=https://youtube.com/watch?v=dQw4w9WgXcQ&format_filter=mp4",
            "headers": {"X-API-Key": "your_api_key"},
            "description": "Get only MP4 formats"
        },
        {
            "title": "Filter by quality",
            "method": "GET",
            "url": "/scrape?url=https://youtube.com/watch?v=dQw4w9WgXcQ&quality_filter=720p",
            "headers": {"X-API-Key": "your_api_key"},
            "description": "Get only 720p quality formats"
        },
        {
            "title": "POST request with JSON",
            "method": "POST",
            "url": "/scrape",
            "headers": {"X-API-Key": "your_api_key", "Content-Type": "application/json"},
            "body": {
                "url": "https://youtube.com/watch?v=dQw4w9WgXcQ",
                "format_filter": "mp4",
                "quality_filter": "720p"
            },
            "description": "POST request with filters"
        }
    ]
    
    for i, example in enumerate(examples, 1):
        print(f"\n{i}. {example['title']}")
        print(f"   Method: {example['method']}")
        print(f"   URL: {example['url']}")
        print(f"   Headers: {example['headers']}")
        if 'body' in example:
            print(f"   Body: {json.dumps(example['body'], indent=8)}")
        print(f"   Description: {example['description']}")


def main():
    """Main demonstration function"""
    demo_scraper()
    demo_api_structure()
    demo_api_usage()
    
    print(f"\n{'=' * 80}")
    print("FLASK API SERVER COMMANDS")
    print(f"{'=' * 80}")
    print("To start the Flask API server:")
    print("  python app.py")
    print()
    print("To test with curl:")
    print("  curl -H 'X-API-Key: robins_secret_key_2024' \\")
    print("       'http://localhost:12000/scrape?url=https://youtube.com/watch?v=dQw4w9WgXcQ'")
    print()
    print("To use the CLI tool:")
    print("  python cli.py 'https://youtube.com/watch?v=dQw4w9WgXcQ' --pretty")
    print()
    print("For production deployment:")
    print("  gunicorn -w 4 -b 0.0.0.0:12000 app:app")
    print(f"{'=' * 80}")


if __name__ == "__main__":
    main()