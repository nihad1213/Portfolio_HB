# app/__init__.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

db = SQLAlchemy()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)

    # App configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///your_database.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'your_secret_key'
    app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'

    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)

    # Import and register blueprints
    from routes.user_routes import userRoutes, dashboardRoutes
    app.register_blueprint(userRoutes, url_prefix='/user')
    app.register_blueprint(dashboardRoutes, url_prefix='/dashboard')

    return app
