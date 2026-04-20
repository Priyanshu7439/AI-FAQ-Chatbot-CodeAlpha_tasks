"""
Vercel Serverless Function Entry Point
Routes all requests to the Flask app
Initialize everything before Vercel runs the function
"""

import os
import sys

# Add parent directory to path so we can import app
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app, initialize_app, FAQ_FILE

# Initialize the app for Vercel
try:
    if os.path.exists(FAQ_FILE):
        initialize_app()
except Exception as e:
    print(f"Warning: {str(e)}")

# Export Flask app for Vercel
export = app.wsgi_app

