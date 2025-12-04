"""
WSGI handler for Vercel serverless functions.
"""
from api.app import app

# Vercel expects the app to be exported as 'app'
# This file will be the entry point for serverless functions
