#!/usr/bin/env python3
"""
Command Line Interface for Media Scraper
"""

import argparse
import json
import sys
from scrapers import MediaScraper


def main():
    """Main CLI function"""
    parser = argparse.ArgumentParser(
        description='Media Scraper CLI - Extract download links from various platforms'
    )
    
    parser.add_argument(
        'url',
        help='URL to scrape'
    )
    
    parser.add_argument(
        '--format',
        help='Filter by format (e.g., mp4, mp3)',
        default=None
    )
    
    parser.add_argument(
        '--quality',
        help='Filter by quality (e.g., 720p, 1080p)',
        default=None
    )
    
    parser.add_argument(
        '--output',
        '-o',
        help='Output file for JSON results',
        default=None
    )
    
    parser.add_argument(
        '--pretty',
        '-p',
        action='store_true',
        help='Pretty print JSON output'
    )
    
    parser.add_argument(
        '--verbose',
        '-v',
        action='store_true',
        help='Verbose output'
    )
    
    args = parser.parse_args()
    
    if args.verbose:
        print(f"Scraping URL: {args.url}")
        if args.format:
            print(f"Format filter: {args.format}")
        if args.quality:
            print(f"Quality filter: {args.quality}")
    
    # Initialize scraper
    scraper = MediaScraper()
    
    try:
        # Scrape the media
        result = scraper.scrape_media(args.url)
        
        # Apply filters if specified
        if result.get('success') and result.get('formats'):
            filtered_formats = result['formats']
            
            if args.format:
                filtered_formats = [
                    fmt for fmt in filtered_formats 
                    if fmt.get('ext', '').lower() == args.format.lower()
                ]
            
            if args.quality:
                filtered_formats = [
                    fmt for fmt in filtered_formats 
                    if args.quality.lower() in fmt.get('quality', '').lower()
                ]
            
            result['formats'] = filtered_formats
            result['total_formats'] = len(filtered_formats)
        
        # Format output
        if args.pretty:
            output = json.dumps(result, indent=2, default=str)
        else:
            output = json.dumps(result, default=str)
        
        # Save to file or print
        if args.output:
            with open(args.output, 'w') as f:
                f.write(output)
            print(f"Results saved to {args.output}")
        else:
            print(output)
        
        # Exit with appropriate code
        if result.get('success'):
            sys.exit(0)
        else:
            if args.verbose:
                print(f"Error: {result.get('error')}", file=sys.stderr)
            sys.exit(1)
            
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()