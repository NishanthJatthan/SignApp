"""
WSGI handler for Vercel serverless functions.
"""
from api.app import app

# Export the Flask app as the handler
handler = app
