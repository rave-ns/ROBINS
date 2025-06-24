# ROBINS - Media Scraper API

A powerful Python-based media scraper that extracts download links from various platforms like YouTube, TikTok, Instagram, and more. Built with Flask API for easy integration.

## Features

- 🎥 **Multi-Platform Support**: YouTube, TikTok, Instagram, Twitter/X, and more
- 🔗 **Multiple Formats**: Extract video, audio, and image links
- 🎛️ **Quality Options**: Get various quality options (720p, 1080p, MP3, etc.)
- 🔐 **API Key Authentication**: Secure access with API keys
- 📊 **JSON Response**: Clean, structured JSON responses
- 🚀 **Production Ready**: Built with Flask and proper error handling
- 🛠️ **CLI Tool**: Command-line interface for direct usage

## Supported Platforms

- **YouTube** (youtube.com, youtu.be)
- **TikTok** (tiktok.com)
- **Instagram** (instagram.com)
- **Twitter/X** (twitter.com, x.com)
- **Generic** (many other platforms via yt-dlp)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd ROBINS
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your API key
```

## Usage

### Flask API

1. Start the server:
```bash
python app.py
```

2. Make requests to the API:

#### GET Request
```bash
curl -H "X-API-Key: your_api_key" \
     "http://localhost:12000/scrape?url=https://youtube.com/watch?v=dQw4w9WgXcQ"
```

#### POST Request
```bash
curl -X POST \
     -H "Content-Type: application/json" \
     -H "X-API-Key: your_api_key" \
     -d '{"url": "https://youtube.com/watch?v=dQw4w9WgXcQ"}' \
     http://localhost:12000/scrape
```

### Command Line Interface

```bash
# Basic usage
python cli.py "https://youtube.com/watch?v=dQw4w9WgXcQ"

# With filters
python cli.py "https://youtube.com/watch?v=dQw4w9WgXcQ" --format mp4 --quality 720p

# Save to file
python cli.py "https://youtube.com/watch?v=dQw4w9WgXcQ" --output results.json --pretty
```

### Python Module

```python
from scrapers import MediaScraper

scraper = MediaScraper()
result = scraper.scrape_media("https://youtube.com/watch?v=dQw4w9WgXcQ")

if result['success']:
    print(f"Title: {result['title']}")
    print(f"Available formats: {len(result['formats'])}")
    for fmt in result['formats']:
        print(f"- {fmt['ext']} | {fmt['quality']} | {fmt['filesize']} bytes")
```

## API Endpoints

### GET /
Returns API documentation and information.

### GET /health
Health check endpoint.

### GET /scrape
Main scraping endpoint.

**Parameters:**
- `url` (required): Media URL to scrape
- `format_filter` (optional): Filter by format (e.g., 'mp4', 'mp3')
- `quality_filter` (optional): Filter by quality (e.g., '720p', '1080p')
- `api_key` (required): API key for authentication

**Headers:**
- `X-API-Key`: API key for authentication (alternative to query parameter)

### POST /scrape
Same as GET /scrape but accepts JSON body:

```json
{
    "url": "https://youtube.com/watch?v=example",
    "format_filter": "mp4",
    "quality_filter": "720p"
}
```

### GET /platforms
Returns information about supported platforms.

## Response Format

```json
{
    "success": true,
    "platform": "youtube",
    "title": "Video Title",
    "description": "Video description",
    "duration": 180,
    "thumbnail": "https://thumbnail-url.jpg",
    "uploader": "Channel Name",
    "upload_date": "20231201",
    "view_count": 1000000,
    "like_count": 50000,
    "formats": [
        {
            "format_id": "22",
            "ext": "mp4",
            "quality": "720p",
            "filesize": 50000000,
            "url": "https://download-url.com/video.mp4",
            "width": 1280,
            "height": 720,
            "fps": 30,
            "tbr": 1000
        }
    ],
    "total_formats": 15,
    "scraped_url": "https://original-url.com",
    "filters_applied": {
        "format": null,
        "quality": null
    }
}
```

## Configuration

Environment variables in `.env`:

```env
API_SECRET_KEY=your_secret_api_key_here
FLASK_ENV=development
FLASK_DEBUG=True
HOST=0.0.0.0
PORT=12000
REQUEST_TIMEOUT=30
MAX_FORMATS=50
```

## Testing

Run the test script:

```bash
python test_scraper.py
```

This will test both the scraper functionality and API endpoints.

## Error Handling

The API returns appropriate HTTP status codes:

- `200`: Success
- `400`: Bad Request (missing URL, invalid format)
- `401`: Unauthorized (missing API key)
- `403`: Forbidden (invalid API key)
- `404`: Not Found (invalid endpoint)
- `500`: Internal Server Error

Error response format:
```json
{
    "success": false,
    "error": "Error description",
    "platform": "youtube"
}
```

## Security

- API key authentication required for all scraping endpoints
- Input validation for URLs and parameters
- Rate limiting can be implemented (configuration ready)
- CORS support for web applications

## Dependencies

- **Flask**: Web framework
- **requests**: HTTP library
- **BeautifulSoup4**: HTML parsing
- **yt-dlp**: Media extraction library
- **python-dotenv**: Environment variable management

## Production Deployment

1. Set environment to production:
```env
FLASK_ENV=production
FLASK_DEBUG=False
```

2. Use a production WSGI server:
```bash
gunicorn -w 4 -b 0.0.0.0:12000 app:app
```

3. Set up reverse proxy (nginx) for SSL and load balancing.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

This project is for educational purposes. Please respect the terms of service of the platforms you're scraping from.

## Disclaimer

This tool is for educational and personal use only. Users are responsible for complying with the terms of service of the platforms they scrape from. The developers are not responsible for any misuse of this tool.