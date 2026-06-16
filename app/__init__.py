from flask import Flask, render_template
from flask_migrate import Migrate
import logging

from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_talisman import Talisman
from app.models import db
from app.config.settings import config_by_name

# Initialize extensions
migrate = Migrate()
limiter = Limiter(key_func=get_remote_address, default_limits=["200 per day", "50 per hour"])
talisman = Talisman()

import os
def create_app(config_name='dev'):
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    app = Flask(__name__, 
                template_folder=os.path.join(base_dir, 'templates'),
                static_folder=os.path.join(base_dir, 'static'))
    
    app.config.from_object(config_by_name[config_name])

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    limiter.init_app(app)
    
    # Configure CSP to allow marked.js, font awesome, google fonts
    csp = {
        'default-src': ["'self'"],
        'script-src': ["'self'", "'unsafe-inline'", "https://cdn.jsdelivr.net"],
        'style-src': ["'self'", "'unsafe-inline'", "https://fonts.googleapis.com", "https://cdnjs.cloudflare.com"],
        'font-src': ["'self'", "https://fonts.gstatic.com", "https://cdnjs.cloudflare.com"],
        'connect-src': ["'self'", "https://api.groq.com"]
    }
    talisman.init_app(app, content_security_policy=csp)

    # Configure logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Register blueprints
    from app.routes.chat_routes import chat_bp
    from app.routes.booking_routes import booking_bp
    
    app.register_blueprint(chat_bp)
    app.register_blueprint(booking_bp)

    # Base route for frontend
    @app.route('/')
    def index():
        return render_template('index.html')

    return app
