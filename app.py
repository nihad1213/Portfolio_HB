#!/usr/bin/env python3

# Importing modules
from flask import Flask, render_template
import secrets
from flask_mysqldb import MySQL
import os
from flask_mail import Mail
from datetime import datetime
from dotenv import load_dotenv
from db import db
from waf import waf_middleware, apply_http_method_restrictions, check_file_uploads

# Load the .env file
load_dotenv()

# Create flask app
app = Flask(__name__)

# Database Config
DATABASE_TYPE = os.getenv('DATABASE_TYPE')
DATABASE_USER_NAME = os.getenv('DATABASE_USER_NAME')
DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD')
DATABASE_NAME = os.getenv('DATABASE_NAME')

# Database URI
app.config['SQLALCHEMY_DATABASE_URI'] = f"{DATABASE_TYPE}://{DATABASE_USER_NAME}:{DATABASE_PASSWORD}@localhost:3306/{DATABASE_NAME}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Fetch configuration from environment variables
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT'))
app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS')
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER')

# Initialize Flask-Mail
mail = Mail(app)

# Importing Models
from models.User import User
from models.Admin import Admin
from models.Attendance import Attendance
from models.Category import Category
from models.Chat import Chat
from models.Event import Event
from models.Ticket import Ticket

# Importing Routes
from routes.footer_routes import footerRoutes, get_current_year
from routes.user_routes import userRoutes
from routes.header_routes import headerRoutes

# Registering blueprints
app.register_blueprint(footerRoutes)
app.register_blueprint(userRoutes)
app.register_blueprint(headerRoutes)

# Apply WAF Middleware to all routes
@app.before_request
def apply_waf():
    """Apply the WAF middleware to every request."""
    waf_middleware()  # Check for SQL Injection, XSS, IP blocking, etc.
    apply_http_method_restrictions()  # Enforce allowed HTTP methods
    check_file_uploads()  # Inspect file uploads for security

# Route for index
@app.route('/')
def index():
    return render_template('index.html', current_year=get_current_year())

# Ensure database tables are created before the app starts
if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(host="0.0.0.0", port=8000, debug=True)
