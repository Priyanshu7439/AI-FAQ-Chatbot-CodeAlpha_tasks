"""
Vercel Serverless Function Entry Point
Routes all requests to the Flask app
"""

from app import app

# Vercel will use this as the serverless function
export = app.wsgi_app
