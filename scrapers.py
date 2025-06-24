"""
Media Scraper Module
Handles scraping of download links from various platforms like YouTube, TikTok, etc.
"""

import re
import json
import requests
from bs4 import BeautifulSoup
import yt_dlp
from typing import Dict, List, Optional, Any
from urllib.parse import urlparse, parse_qs
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MediaScraper:
    """Main scraper class for handling different media platforms"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
    
    def identify_platform(self, url: str) -> str:
        """Identify the platform from URL"""
        domain = urlparse(url).netloc.lower()
        
        if 'youtube.com' in domain or 'youtu.be' in domain:
            return 'youtube'
        elif 'tiktok.com' in domain:
            return 'tiktok'
        elif 'instagram.com' in domain:
            return 'instagram'
        elif 'twitter.com' in domain or 'x.com' in domain:
            return 'twitter'
        else:
            return 'unknown'
    
    def scrape_media(self, url: str) -> Dict[str, Any]:
        """Main method to scrape media from any supported platform"""
        try:
            platform = self.identify_platform(url)
            
            if platform == 'youtube':
                return self.scrape_youtube(url)
            elif platform == 'tiktok':
                return self.scrape_tiktok(url)
            elif platform == 'instagram':
                return self.scrape_instagram(url)
            elif platform == 'twitter':
                return self.scrape_twitter(url)
            else:
                # Try generic yt-dlp approach for unknown platforms
                return self.scrape_with_ytdlp(url)
                
        except Exception as e:
            logger.error(f"Error scraping {url}: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'platform': platform if 'platform' in locals() else 'unknown'
            }
    
    def scrape_youtube(self, url: str) -> Dict[str, Any]:
        """Scrape YouTube videos using yt-dlp"""
        try:
            ydl_opts = {
                'quiet': True,
                'no_warnings': True,
                'extract_flat': False,
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                
                formats = []
                for fmt in info.get('formats', []):
                    if fmt.get('url'):
                        format_info = {
                            'format_id': fmt.get('format_id'),
                            'ext': fmt.get('ext'),
                            'quality': fmt.get('format_note', 'Unknown'),
                            'filesize': fmt.get('filesize'),
                            'url': fmt.get('url'),
                            'vcodec': fmt.get('vcodec'),
                            'acodec': fmt.get('acodec'),
                            'width': fmt.get('width'),
                            'height': fmt.get('height'),
                            'fps': fmt.get('fps'),
                            'tbr': fmt.get('tbr')  # total bitrate
                        }
                        formats.append(format_info)
                
                return {
                    'success': True,
                    'platform': 'youtube',
                    'title': info.get('title'),
                    'description': info.get('description'),
                    'duration': info.get('duration'),
                    'thumbnail': info.get('thumbnail'),
                    'uploader': info.get('uploader'),
                    'upload_date': info.get('upload_date'),
                    'view_count': info.get('view_count'),
                    'like_count': info.get('like_count'),
                    'formats': formats
                }
                
        except Exception as e:
            logger.error(f"YouTube scraping error: {str(e)}")
            return {
                'success': False,
                'error': f"YouTube scraping failed: {str(e)}",
                'platform': 'youtube'
            }
    
    def scrape_tiktok(self, url: str) -> Dict[str, Any]:
        """Scrape TikTok videos using yt-dlp as primary method"""
        try:
            # First try with yt-dlp
            ydl_opts = {
                'quiet': True,
                'no_warnings': True,
                'extract_flat': False,
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                
                formats = []
                for fmt in info.get('formats', []):
                    if fmt.get('url'):
                        format_info = {
                            'format_id': fmt.get('format_id'),
                            'ext': fmt.get('ext'),
                            'quality': fmt.get('format_note', 'Unknown'),
                            'filesize': fmt.get('filesize'),
                            'url': fmt.get('url'),
                            'width': fmt.get('width'),
                            'height': fmt.get('height'),
                            'tbr': fmt.get('tbr')
                        }
                        formats.append(format_info)
                
                return {
                    'success': True,
                    'platform': 'tiktok',
                    'title': info.get('title'),
                    'description': info.get('description'),
                    'duration': info.get('duration'),
                    'thumbnail': info.get('thumbnail'),
                    'uploader': info.get('uploader'),
                    'upload_date': info.get('upload_date'),
                    'view_count': info.get('view_count'),
                    'like_count': info.get('like_count'),
                    'formats': formats
                }
                
        except Exception as e:
            logger.error(f"TikTok yt-dlp error: {str(e)}")
            # Fallback to manual scraping
            return self.scrape_tiktok_manual(url)
    
    def scrape_tiktok_manual(self, url: str) -> Dict[str, Any]:
        """Manual TikTok scraping using requests and BeautifulSoup"""
        try:
            response = self.session.get(url)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Try to find JSON data in script tags
            script_tags = soup.find_all('script', {'id': '__UNIVERSAL_DATA_FOR_REHYDRATION__'})
            
            if script_tags:
                script_content = script_tags[0].string
                try:
                    data = json.loads(script_content)
                    # Extract video information from the JSON structure
                    # This is a simplified extraction - TikTok's structure changes frequently
                    video_data = self.extract_tiktok_data(data)
                    if video_data:
                        return video_data
                except json.JSONDecodeError:
                    pass
            
            # Fallback: try to extract basic information
            title_tag = soup.find('title')
            title = title_tag.text if title_tag else "TikTok Video"
            
            # Look for meta tags with video information
            og_video = soup.find('meta', {'property': 'og:video'})
            og_image = soup.find('meta', {'property': 'og:image'})
            
            formats = []
            if og_video and og_video.get('content'):
                formats.append({
                    'format_id': 'mp4',
                    'ext': 'mp4',
                    'quality': 'default',
                    'url': og_video['content']
                })
            
            return {
                'success': True,
                'platform': 'tiktok',
                'title': title,
                'thumbnail': og_image['content'] if og_image else None,
                'formats': formats
            }
            
        except Exception as e:
            logger.error(f"TikTok manual scraping error: {str(e)}")
            return {
                'success': False,
                'error': f"TikTok scraping failed: {str(e)}",
                'platform': 'tiktok'
            }
    
    def extract_tiktok_data(self, data: Dict) -> Optional[Dict[str, Any]]:
        """Extract video data from TikTok's JSON structure"""
        try:
            # This is a simplified extraction - actual structure may vary
            # You would need to analyze TikTok's current JSON structure
            return None
        except Exception:
            return None
    
    def scrape_instagram(self, url: str) -> Dict[str, Any]:
        """Scrape Instagram content using yt-dlp"""
        try:
            ydl_opts = {
                'quiet': True,
                'no_warnings': True,
                'extract_flat': False,
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                
                formats = []
                for fmt in info.get('formats', []):
                    if fmt.get('url'):
                        format_info = {
                            'format_id': fmt.get('format_id'),
                            'ext': fmt.get('ext'),
                            'quality': fmt.get('format_note', 'Unknown'),
                            'filesize': fmt.get('filesize'),
                            'url': fmt.get('url'),
                            'width': fmt.get('width'),
                            'height': fmt.get('height')
                        }
                        formats.append(format_info)
                
                return {
                    'success': True,
                    'platform': 'instagram',
                    'title': info.get('title'),
                    'description': info.get('description'),
                    'thumbnail': info.get('thumbnail'),
                    'uploader': info.get('uploader'),
                    'formats': formats
                }
                
        except Exception as e:
            logger.error(f"Instagram scraping error: {str(e)}")
            return {
                'success': False,
                'error': f"Instagram scraping failed: {str(e)}",
                'platform': 'instagram'
            }
    
    def scrape_twitter(self, url: str) -> Dict[str, Any]:
        """Scrape Twitter/X content using yt-dlp"""
        try:
            ydl_opts = {
                'quiet': True,
                'no_warnings': True,
                'extract_flat': False,
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                
                formats = []
                for fmt in info.get('formats', []):
                    if fmt.get('url'):
                        format_info = {
                            'format_id': fmt.get('format_id'),
                            'ext': fmt.get('ext'),
                            'quality': fmt.get('format_note', 'Unknown'),
                            'filesize': fmt.get('filesize'),
                            'url': fmt.get('url'),
                            'width': fmt.get('width'),
                            'height': fmt.get('height')
                        }
                        formats.append(format_info)
                
                return {
                    'success': True,
                    'platform': 'twitter',
                    'title': info.get('title'),
                    'description': info.get('description'),
                    'thumbnail': info.get('thumbnail'),
                    'uploader': info.get('uploader'),
                    'formats': formats
                }
                
        except Exception as e:
            logger.error(f"Twitter scraping error: {str(e)}")
            return {
                'success': False,
                'error': f"Twitter scraping failed: {str(e)}",
                'platform': 'twitter'
            }
    
    def scrape_with_ytdlp(self, url: str) -> Dict[str, Any]:
        """Generic scraping using yt-dlp for unknown platforms"""
        try:
            ydl_opts = {
                'quiet': True,
                'no_warnings': True,
                'extract_flat': False,
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                
                formats = []
                for fmt in info.get('formats', []):
                    if fmt.get('url'):
                        format_info = {
                            'format_id': fmt.get('format_id'),
                            'ext': fmt.get('ext'),
                            'quality': fmt.get('format_note', 'Unknown'),
                            'filesize': fmt.get('filesize'),
                            'url': fmt.get('url'),
                            'width': fmt.get('width'),
                            'height': fmt.get('height')
                        }
                        formats.append(format_info)
                
                return {
                    'success': True,
                    'platform': 'generic',
                    'title': info.get('title'),
                    'description': info.get('description'),
                    'thumbnail': info.get('thumbnail'),
                    'uploader': info.get('uploader'),
                    'formats': formats
                }
                
        except Exception as e:
            logger.error(f"Generic scraping error: {str(e)}")
            return {
                'success': False,
                'error': f"Generic scraping failed: {str(e)}",
                'platform': 'generic'
            }


def test_scrapers():
    """Test function to verify scraper functionality"""
    scraper = MediaScraper()
    
    # Test URLs (replace with actual test URLs)
    test_urls = [
        "https://www.youtube.com/watch?v=dQw4w9WgXcQ",  # Rick Roll
        # Add more test URLs as needed
    ]
    
    for url in test_urls:
        print(f"\nTesting: {url}")
        result = scraper.scrape_media(url)
        print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    test_scrapers()