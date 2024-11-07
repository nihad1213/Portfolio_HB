#!/usr/bin/env python3

# Import necessary modules
from flask import Flask, render_template
from flask_mysqldb import MySQL
import os
from flask_mail import Mail
from datetime import timedelta
from dotenv import load_dotenv
from db import db
from flask_jwt_extended import JWTManager
from models.Admin import Admin
from waf import waf_middleware, enforce_allowed_methods, check_file_uploads

# Load environment variables from .env file
load_dotenv()

# Create the Flask app
app = Flask(__name__)

# JWT configuration
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)

# Initialize the JWT Manager
jwt = JWTManager(app)

# Database configuration
DATABASE_TYPE = os.getenv('DATABASE_TYPE')
DATABASE_USER_NAME = os.getenv('DATABASE_USER_NAME')
DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD')
DATABASE_NAME = os.getenv('DATABASE_NAME')

# SQLAlchemy Database URI
app.config['SQLALCHEMY_DATABASE_URI'] = f"{DATABASE_TYPE}://{DATABASE_USER_NAME}:{DATABASE_PASSWORD}@localhost:3306/{DATABASE_NAME}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy with the Flask app
db.init_app(app)

# Mail configuration
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT'))
app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS')
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER')

# Initialize Flask-Mail
mail = Mail(app)

# Importing models
from models.User import User
from models.Attendance import Attendance
from models.Category import Category
from models.Chat import Chat
from models.Event import Event
from models.Ticket import Ticket
from models.Subscriber import Subscribers

# Import routes
from routes.footer_routes import footerRoutes, get_current_year
from routes.user_routes import userRoutes
from routes.header_routes import headerRoutes
from routes.main_routes import mainRoutes
from routes.profile_routes import profileRoutes
from routes.admin_routes import adminRoutes

# Registering blueprints for different route modules
app.register_blueprint(footerRoutes)
app.register_blueprint(userRoutes)
app.register_blueprint(headerRoutes)
app.register_blueprint(mainRoutes)
app.register_blueprint(profileRoutes)
app.register_blueprint(adminRoutes)

# Apply WAF Middleware to all incoming requests
@app.before_request
def apply_waf():
    """Apply the WAF middleware to every request."""
    waf_middleware()  # Checks for SQL Injection, XSS, IP blocking, etc.
    enforce_allowed_methods(['GET', 'POST'])  # Enforce allowed HTTP methods (modify as needed)
    check_file_uploads()  # Inspect file uploads for security

# Route for the index page
@app.route('/')
def index():
    events = Event.query.filter_by(status=1).order_by(Event.likes.desc()).limit(3).all()
    return render_template('index.html', current_year=get_current_year(), events=events)

# Ensure that the database tables are created before the app starts
if __name__ == "__main__":
    with app.app_context():
        db.create_all()

        # Check if the admin already exists
        admin_username = "admin"
        admin_email = "admin@fest.com"
        admin_password = "admin"

        admin = Admin.query.filter_by(username=admin_username).first()

        if not admin:
            # Create a new admin with automatic password hashing
            new_admin = Admin(username=admin_username, email=admin_email, password=admin_password)
            new_admin.save()
            print(f"Admin user {admin_username} created successfully.")
        else:
            print(f"Admin user {admin_username} already exists.")

    # Start the app on port 8000 with debugging enabled
    app.run(host="0.0.0.0", port=8000, debug=True)
