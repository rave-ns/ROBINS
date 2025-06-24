#!/usr/bin/env python3
"""
Production server startup script
"""

import os
import sys
import argparse
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def start_development_server(host='0.0.0.0', port=12000):
    """Start development server"""
    print(f"Starting development server on {host}:{port}")
    
    # Set environment variables
    os.environ['FLASK_ENV'] = 'development'
    os.environ['FLASK_DEBUG'] = 'True'
    os.environ['HOST'] = host
    os.environ['PORT'] = str(port)
    
    # Import and run the app
    from app import app
    app.run(host=host, port=port, debug=True, threaded=True)


def start_production_server(host='0.0.0.0', port=12000, workers=4):
    """Start production server with gunicorn"""
    print(f"Starting production server on {host}:{port} with {workers} workers")
    
    # Set environment variables
    os.environ['FLASK_ENV'] = 'production'
    os.environ['FLASK_DEBUG'] = 'False'
    os.environ['HOST'] = host
    os.environ['PORT'] = str(port)
    
    # Start gunicorn
    import subprocess
    cmd = [
        'gunicorn',
        '--workers', str(workers),
        '--bind', f'{host}:{port}',
        '--timeout', '120',
        '--keep-alive', '5',
        '--max-requests', '1000',
        '--max-requests-jitter', '100',
        '--preload',
        'app:app'
    ]
    
    subprocess.run(cmd)


def main():
    """Main function"""
    parser = argparse.ArgumentParser(description='Start Media Scraper API server')
    
    parser.add_argument(
        '--mode',
        choices=['dev', 'prod'],
        default='dev',
        help='Server mode (dev or prod)'
    )
    
    parser.add_argument(
        '--host',
        default='0.0.0.0',
        help='Host to bind to'
    )
    
    parser.add_argument(
        '--port',
        type=int,
        default=12000,
        help='Port to bind to'
    )
    
    parser.add_argument(
        '--workers',
        type=int,
        default=4,
        help='Number of workers (production mode only)'
    )
    
    args = parser.parse_args()
    
    # Check if API key is set
    api_key = os.getenv('API_SECRET_KEY')
    if not api_key or api_key == 'your_secret_api_key_here':
        print("WARNING: API_SECRET_KEY not set or using default value!")
        print("Please set a secure API key in your .env file")
        if args.mode == 'prod':
            print("Exiting for security reasons in production mode")
            sys.exit(1)
    
    try:
        if args.mode == 'dev':
            start_development_server(args.host, args.port)
        else:
            start_production_server(args.host, args.port, args.workers)
    except KeyboardInterrupt:
        print("\nServer stopped by user")
    except Exception as e:
        print(f"Error starting server: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()