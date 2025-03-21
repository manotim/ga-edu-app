from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_cors import CORS
from app.routes import mpesa_bp

import os

db = SQLAlchemy()
jwt = JWTManager()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    
    # Register Blueprints
    app.register_blueprint(mpesa_bp)

    # Load configuration from config.py
    app.config.from_object("config.Config")

    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)
    CORS(app)

    # Register blueprints (routes)
    from app.auth import auth_bp
    from app.routes import main_bp

    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(main_bp, url_prefix="/api")

    # ✅ Default Route to Avoid 404 Errors
    @app.route("/")
    def home():
        return jsonify({"message": "Welcome to Edu House!"})

    # ✅ Debug Route
    @app.route("/test")
    def test():
        return jsonify({"message": "Test route is working!"})

    return app
