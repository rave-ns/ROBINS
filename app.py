"""
Flask API for Media Scraping
Provides endpoints to scrape download links from various media platforms
"""

import os
import json
from functools import wraps
from flask import Flask, request, jsonify, abort
from dotenv import load_dotenv
from scrapers import MediaScraper
import logging

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

# Initialize scraper
scraper = MediaScraper()

# API Configuration
API_SECRET_KEY = os.getenv('API_SECRET_KEY', 'default_secret_key')


def require_api_key(f):
    """Decorator to require API key authentication"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('X-API-Key') or request.args.get('api_key')
        
        if not api_key:
            return jsonify({
                'success': False,
                'error': 'API key is required. Provide it in X-API-Key header or api_key parameter.'
            }), 401
        
        if api_key != API_SECRET_KEY:
            return jsonify({
                'success': False,
                'error': 'Invalid API key.'
            }), 403
        
        return f(*args, **kwargs)
    return decorated_function


@app.route('/')
def index():
    """API documentation endpoint"""
    return jsonify({
        'name': 'Media Scraper API',
        'version': '1.0.0',
        'description': 'API for scraping download links from various media platforms',
        'endpoints': {
            '/scrape': {
                'method': 'GET',
                'description': 'Scrape media from a URL',
                'parameters': {
                    'url': 'Media URL to scrape (required)',
                    'api_key': 'API key for authentication (required)'
                },
                'example': '/scrape?url=https://youtube.com/watch?v=example&api_key=your_key'
            },
            '/health': {
                'method': 'GET',
                'description': 'Health check endpoint'
            }
        },
        'supported_platforms': [
            'YouTube',
            'TikTok',
            'Instagram',
            'Twitter/X',
            'Generic (via yt-dlp)'
        ]
    })


@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'message': 'Media Scraper API is running'
    })


@app.route('/scrape', methods=['GET'])
@require_api_key
def scrape_media():
    """
    Main endpoint to scrape media from various platforms
    
    Query Parameters:
    - url: The media URL to scrape (required)
    - format_filter: Optional filter for specific formats (e.g., 'mp4', 'mp3')
    - quality_filter: Optional filter for quality (e.g., '720p', '1080p')
    """
    try:
        # Get URL parameter
        url = request.args.get('url')
        if not url:
            return jsonify({
                'success': False,
                'error': 'URL parameter is required'
            }), 400
        
        # Validate URL format
        if not url.startswith(('http://', 'https://')):
            return jsonify({
                'success': False,
                'error': 'Invalid URL format. URL must start with http:// or https://'
            }), 400
        
        # Get optional filters
        format_filter = request.args.get('format_filter')
        quality_filter = request.args.get('quality_filter')
        
        logger.info(f"Scraping URL: {url}")
        
        # Scrape the media
        result = scraper.scrape_media(url)
        
        # Apply filters if specified
        if result.get('success') and result.get('formats'):
            filtered_formats = result['formats']
            
            if format_filter:
                filtered_formats = [
                    fmt for fmt in filtered_formats 
                    if fmt.get('ext', '').lower() == format_filter.lower()
                ]
            
            if quality_filter:
                filtered_formats = [
                    fmt for fmt in filtered_formats 
                    if quality_filter.lower() in fmt.get('quality', '').lower()
                ]
            
            result['formats'] = filtered_formats
            result['total_formats'] = len(filtered_formats)
        
        # Add metadata
        result['scraped_url'] = url
        result['filters_applied'] = {
            'format': format_filter,
            'quality': quality_filter
        }
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Error in scrape_media endpoint: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'Internal server error: {str(e)}'
        }), 500


@app.route('/scrape', methods=['POST'])
@require_api_key
def scrape_media_post():
    """
    POST endpoint for scraping media (for bulk requests or complex parameters)
    
    JSON Body:
    {
        "url": "media_url",
        "format_filter": "optional_format",
        "quality_filter": "optional_quality"
    }
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                'success': False,
                'error': 'JSON body is required'
            }), 400
        
        url = data.get('url')
        if not url:
            return jsonify({
                'success': False,
                'error': 'URL is required in JSON body'
            }), 400
        
        # Validate URL format
        if not url.startswith(('http://', 'https://')):
            return jsonify({
                'success': False,
                'error': 'Invalid URL format. URL must start with http:// or https://'
            }), 400
        
        format_filter = data.get('format_filter')
        quality_filter = data.get('quality_filter')
        
        logger.info(f"Scraping URL (POST): {url}")
        
        # Scrape the media
        result = scraper.scrape_media(url)
        
        # Apply filters if specified
        if result.get('success') and result.get('formats'):
            filtered_formats = result['formats']
            
            if format_filter:
                filtered_formats = [
                    fmt for fmt in filtered_formats 
                    if fmt.get('ext', '').lower() == format_filter.lower()
                ]
            
            if quality_filter:
                filtered_formats = [
                    fmt for fmt in filtered_formats 
                    if quality_filter.lower() in fmt.get('quality', '').lower()
                ]
            
            result['formats'] = filtered_formats
            result['total_formats'] = len(filtered_formats)
        
        # Add metadata
        result['scraped_url'] = url
        result['filters_applied'] = {
            'format': format_filter,
            'quality': quality_filter
        }
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Error in scrape_media_post endpoint: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'Internal server error: {str(e)}'
        }), 500


@app.route('/platforms')
@require_api_key
def get_supported_platforms():
    """Get list of supported platforms"""
    return jsonify({
        'success': True,
        'supported_platforms': {
            'youtube': {
                'name': 'YouTube',
                'domains': ['youtube.com', 'youtu.be'],
                'supported_formats': ['mp4', 'webm', 'mp3', 'm4a']
            },
            'tiktok': {
                'name': 'TikTok',
                'domains': ['tiktok.com'],
                'supported_formats': ['mp4']
            },
            'instagram': {
                'name': 'Instagram',
                'domains': ['instagram.com'],
                'supported_formats': ['mp4', 'jpg']
            },
            'twitter': {
                'name': 'Twitter/X',
                'domains': ['twitter.com', 'x.com'],
                'supported_formats': ['mp4']
            },
            'generic': {
                'name': 'Generic (via yt-dlp)',
                'description': 'Supports many other platforms via yt-dlp',
                'supported_formats': ['various']
            }
        }
    })


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        'success': False,
        'error': 'Endpoint not found'
    }), 404


@app.errorhandler(405)
def method_not_allowed(error):
    """Handle 405 errors"""
    return jsonify({
        'success': False,
        'error': 'Method not allowed'
    }), 405


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({
        'success': False,
        'error': 'Internal server error'
    }), 500


if __name__ == '__main__':
    port = int(os.getenv('PORT', 12000))
    debug = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    
    logger.info(f"Starting Media Scraper API on port {port}")
    logger.info(f"Debug mode: {debug}")
    logger.info(f"API Key required: {API_SECRET_KEY}")
    
    app.run(
        host='0.0.0.0',
        port=port,
        debug=debug,
        threaded=True
    )