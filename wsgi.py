"""
WSGI application entry point for Vercel.
Vercel will automatically detect and use this file.
"""
import sys
import os

# Add the api directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'api'))

from app import app

# For Vercel serverless functions
application = app
