#!/usr/bin/env python3

# Importing modules
from flask import Flask, render_template
import secrets
from flask_mail import Mail
from datetime import datetime
from dotenv import load_dotenv
import os

# Load the .env file
load_dotenv()

# Create flask app
app = Flask(__name__)

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

# importing Routes
from routes.footer_routes import footerRoutes, get_current_year
from routes.user_routes import userRoutes

# Registering blueprints
app.register_blueprint(footerRoutes)
app.register_blueprint(userRoutes)

# Route for index
@app.route('/')
def index():
    return render_template('index.html', current_year=get_current_year())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)