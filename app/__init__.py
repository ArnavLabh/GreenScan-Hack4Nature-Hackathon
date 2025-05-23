from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os
from datetime import timedelta
from sqlalchemy import event
from sqlalchemy.engine import Engine
import sqlite3
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

db = SQLAlchemy()
login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):
    from app.models import User
    return User.query.get(int(user_id))

def create_app():
    app = Flask(__name__)
    
    # Configuration
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'd4e0e9c16ccc43806865ea863b7c8178651fdb5edeb564789751d5219bcc0ad2')
    
    # Database configuration
    if os.environ.get('VERCEL_ENV') == 'production':
        # For production, use a persistent database URL
        database_url = os.environ.get('DATABASE_URL')
        if not database_url:
            logger.error("DATABASE_URL not set in production environment")
            database_url = 'sqlite:///app.db'
        
        if database_url.startswith('postgres://'):
            database_url = database_url.replace('postgres://', 'postgresql://', 1)
        
        app.config['SQLALCHEMY_DATABASE_URI'] = database_url
        logger.info(f"Using production database: {database_url}")
    else:
        # For development, use SQLite
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
        logger.info("Using development database: sqlite:///app.db")
    
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        'pool_pre_ping': True,
        'pool_recycle': 300,
        'pool_timeout': 30,
        'max_overflow': 2,
        'pool_size': 1
    }
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)  # 7 days
    app.config['SESSION_COOKIE_SECURE'] = True
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
    
    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'main.login'
    login_manager.login_message_category = 'info'
    
    # Register blueprints
    from app.routes import main
    app.register_blueprint(main)
    
    # Create database tables
    with app.app_context():
        try:
            logger.info("Attempting to create database tables...")
            db.create_all()
            logger.info("Database tables created successfully")
        except Exception as e:
            logger.error(f"Error creating database tables: {str(e)}")
            logger.error(f"Error type: {type(e)}")
    
    @app.errorhandler(500)
    def handle_500_error(e):
        logger.error(f"500 error occurred: {str(e)}")
        return "Internal Server Error", 500
    
    @app.errorhandler(Exception)
    def handle_exception(e):
        logger.error(f"Unhandled exception: {str(e)}")
        return "Internal Server Error", 500
    
    return app

from app import models