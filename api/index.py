import os
import sys

# Ensure the app directory is in the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app

# Vercel provides a serverless environment; typically we want production settings here.
# We also set VERCEL=1 so the app knows it's in a serverless context if needed.
os.environ['VERCEL'] = '1'
env = os.getenv('FLASK_ENV', 'prod')

# This is the WSGI entrypoint that Vercel looks for.
app = create_app(env)
