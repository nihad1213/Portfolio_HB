#!/usr/bin/env python3

# Importing modules
from flask import Flask, render_template, redirect, url_for, session, request, jsonify
from flask_mysqldb import MySQL
import os
from flask_mail import Mail
from datetime import timedelta
from dotenv import load_dotenv
from db import db
from flask_jwt_extended import JWTManager
from models.Admin import Admin
from flask_migrate import Migrate
from oauthlib.oauth2 import WebApplicationClient
import requests
import json

# Load the .env file
load_dotenv()

# Create flask app
app = Flask(__name__)

app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)

# Initialize JWT Manager
jwt = JWTManager(app)

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

# Google OAuth 2.0 setup
GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')  # Add to your .env
GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')  # Add to your .env
GOOGLE_DISCOVERY_URL = "https://accounts.google.com/.well-known/openid-configuration"

client = WebApplicationClient(GOOGLE_CLIENT_ID)

def get_google_provider_cfg():
    return requests.get(GOOGLE_DISCOVERY_URL).json()

# Importing Models
from models.User import User
from models.Attendance import Attendance
from models.Category import Category
from models.Chat import Chat
from models.Event import Event
from models.Ticket import Ticket
from models.Subscriber import Subscribers

migrate = Migrate(app, db)

# Importing Routes
from routes.footer_routes import footerRoutes, get_current_year
from routes.user_routes import userRoutes, dashboardRoutes
from routes.header_routes import headerRoutes
from routes.main_routes import mainRoutes
from routes.profile_routes import profileRoutes
from routes.admin_routes import adminRoutes

# Registering blueprints
app.register_blueprint(footerRoutes)
app.register_blueprint(userRoutes)
app.register_blueprint(headerRoutes)
app.register_blueprint(dashboardRoutes)
app.register_blueprint(mainRoutes)
app.register_blueprint(profileRoutes)
app.register_blueprint(adminRoutes)

# Google Login Route
@app.route("/login")
def login():
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]

    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=request.base_url + "/callback",
        scope=["openid", "email", "profile"],
    )
    return redirect(request_uri)


# Google OAuth callback route
@app.route("/login/callback")
def callback():
    # Get authorization code Google sent back to you
    code = request.args.get("code")

    google_provider_cfg = get_google_provider_cfg()
    token_endpoint = google_provider_cfg["token_endpoint"]

    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code
    )
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET),
    )

    # Parse the tokens!
    client.parse_request_body_response(json.dumps(token_response.json()))

    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)

    # Verify the user's email is verified by Google
    if userinfo_response.json().get("email_verified"):
        users_email = userinfo_response.json()["email"]
        users_name = userinfo_response.json()["given_name"]
        users_picture = userinfo_response.json()["picture"]

        # Store user info in the session
        session["email"] = users_email
        session["name"] = users_name
        session["picture"] = users_picture

        return redirect(url_for("dashboard"))
    else:
        return "User email not available or not verified by Google.", 400

# Route for user dashboard after login
@app.route("/dashboard")
def dashboard():
    if "email" not in session:
        return redirect(url_for("login"))

    user_info = {
        "name": session["name"],
        "email": session["email"],
        "picture": session["picture"]
    }

    return render_template("dashboard.html", user=user_info)

# Route for index
@app.route('/')
def index():
    return render_template('index.html', current_year=get_current_year())

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

    app.run(host="0.0.0.0", port=8000, debug=True)
