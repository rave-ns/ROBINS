#!/usr/bin/env python3
"""
Comprehensive test suite for the Media Scraper project
"""

import sys
import json
import time
import subprocess
from scrapers import MediaScraper


def test_scraper_functionality():
    """Test the core scraper functionality"""
    print("=" * 60)
    print("TESTING SCRAPER FUNCTIONALITY")
    print("=" * 60)
    
    scraper = MediaScraper()
    
    # Test platform identification
    print("\n1. Testing platform identification...")
    test_urls = {
        "https://www.youtube.com/watch?v=dQw4w9WgXcQ": "youtube",
        "https://youtu.be/dQw4w9WgXcQ": "youtube",
        "https://www.tiktok.com/@user/video/123": "tiktok",
        "https://www.instagram.com/p/example/": "instagram",
        "https://twitter.com/user/status/123": "twitter",
        "https://x.com/user/status/123": "twitter",
        "https://example.com/video": "unknown"
    }
    
    for url, expected in test_urls.items():
        result = scraper.identify_platform(url)
        status = "✅" if result == expected else "❌"
        print(f"  {status} {url[:40]:<40} -> {result} (expected: {expected})")
    
    # Test actual scraping
    print("\n2. Testing YouTube scraping...")
    try:
        result = scraper.scrape_media("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
        if result.get('success'):
            print(f"  ✅ Successfully scraped: {result.get('title', 'N/A')[:50]}...")
            print(f"  ✅ Platform: {result.get('platform')}")
            print(f"  ✅ Formats: {len(result.get('formats', []))}")
            print(f"  ✅ Duration: {result.get('duration')} seconds")
        else:
            print(f"  ❌ Scraping failed: {result.get('error')}")
            return False
    except Exception as e:
        print(f"  ❌ Exception during scraping: {str(e)}")
        return False
    
    return True


def test_cli_tool():
    """Test the CLI tool"""
    print("\n" + "=" * 60)
    print("TESTING CLI TOOL")
    print("=" * 60)
    
    try:
        # Test CLI help
        print("\n1. Testing CLI help...")
        result = subprocess.run([sys.executable, 'cli.py', '--help'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print("  ✅ CLI help works")
        else:
            print("  ❌ CLI help failed")
            return False
        
        # Test CLI scraping
        print("\n2. Testing CLI scraping...")
        result = subprocess.run([
            sys.executable, 'cli.py', 
            'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
            '--pretty'
        ], capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            try:
                output = json.loads(result.stdout)
                if output.get('success'):
                    print(f"  ✅ CLI scraping successful: {output.get('title', 'N/A')[:50]}...")
                else:
                    print(f"  ❌ CLI scraping failed: {output.get('error')}")
                    return False
            except json.JSONDecodeError:
                print("  ❌ CLI output is not valid JSON")
                return False
        else:
            print(f"  ❌ CLI command failed: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"  ❌ CLI test exception: {str(e)}")
        return False
    
    return True


def test_imports():
    """Test all imports work correctly"""
    print("\n" + "=" * 60)
    print("TESTING IMPORTS")
    print("=" * 60)
    
    modules = [
        ('scrapers', 'MediaScraper'),
        ('app', 'app'),
        ('config', 'Config'),
        ('cli', None)
    ]
    
    for module_name, class_name in modules:
        try:
            module = __import__(module_name)
            if class_name:
                getattr(module, class_name)
            print(f"  ✅ {module_name} imports successfully")
        except Exception as e:
            print(f"  ❌ {module_name} import failed: {str(e)}")
            return False
    
    return True


def test_dependencies():
    """Test that all required dependencies are available"""
    print("\n" + "=" * 60)
    print("TESTING DEPENDENCIES")
    print("=" * 60)
    
    dependencies = [
        'flask',
        'requests',
        'bs4',
        'yt_dlp',
        'lxml',
        'dotenv',
        'gunicorn'
    ]
    
    for dep in dependencies:
        try:
            __import__(dep)
            print(f"  ✅ {dep} is available")
        except ImportError:
            print(f"  ❌ {dep} is missing")
            return False
    
    return True


def test_configuration():
    """Test configuration loading"""
    print("\n" + "=" * 60)
    print("TESTING CONFIGURATION")
    print("=" * 60)
    
    try:
        from config import Config
        config = Config()
        
        print(f"  ✅ Config loaded successfully")
        print(f"  ✅ API Key: {'*' * len(config.API_SECRET_KEY) if config.API_SECRET_KEY else 'Not set'}")
        print(f"  ✅ Debug mode: {config.DEBUG}")
        print(f"  ✅ Host: {config.HOST}")
        print(f"  ✅ Port: {config.PORT}")
        
        return True
    except Exception as e:
        print(f"  ❌ Configuration test failed: {str(e)}")
        return False


def main():
    """Run all tests"""
    print("ROBINS MEDIA SCRAPER - COMPREHENSIVE TEST SUITE")
    print("=" * 80)
    
    tests = [
        ("Dependencies", test_dependencies),
        ("Imports", test_imports),
        ("Configuration", test_configuration),
        ("Scraper Functionality", test_scraper_functionality),
        ("CLI Tool", test_cli_tool),
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        print(f"\nRunning {test_name} tests...")
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"❌ {test_name} test suite failed with exception: {str(e)}")
            results[test_name] = False
    
    # Summary
    print("\n" + "=" * 80)
    print("TEST RESULTS SUMMARY")
    print("=" * 80)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{test_name:<25} {status}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{total} test suites passed")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED! The Media Scraper is ready to use.")
        return 0
    else:
        print("⚠️  Some tests failed. Please check the output above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())