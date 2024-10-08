#!/usr/bin/env python3

from flask import Blueprint, render_template, request, flash, redirect, url_for
from models.User import User, db
from itsdangerous import URLSafeTimedSerializer
from flask_mail import Mail, Message
import os
import logging
from dotenv import load_dotenv
from werkzeug.utils import secure_filename
import time

# Load environment variables from .env file
load_dotenv()

# Initialize Flask-Mail
mail = Mail()

SECRET_KEY = os.getenv('SECRET_KEY')
s = URLSafeTimedSerializer(SECRET_KEY)

profileRoutes = Blueprint('profile_routes', __name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
UPLOAD_FOLDER = 'static/user'

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@profileRoutes.route('/profile/<user_id>', methods=['GET', 'POST'])
def profile(user_id):
    logger.debug(f"Profile route accessed for user_id: {user_id}")
    user = User.query.get(user_id)

    if user is None:
        logger.warning(f"User not found for user_id: {user_id}")
        flash('User not found.', 'danger')
        return redirect(url_for('home'))

    if request.method == 'POST':
        logger.debug("POST request received")
        user.name = request.form['firstName']
        user.surname = request.form['lastName']
        user.description = request.form['description']
        user.phone_number = request.form['phoneNumber']

        logger.debug(f"Form data: {request.form}")
        logger.debug(f"Files in request: {request.files}")

        if 'profilePicInput' in request.files:
            file = request.files['profilePicInput']
            if file and file.filename != '' and allowed_file(file.filename):
                filename = save_file(file)
                if filename:
                    user.profile_image = filename
                    logger.info(f"User profile image updated to: {user.profile_image}")
                else:
                    logger.warning("Failed to save the image")
                    flash('Failed to save the image', 'danger')
            else:
                logger.warning("Invalid file or no file selected")
        else:
            logger.warning("No file found in request")

        try:
            db.session.commit()
            logger.info("Database updated successfully")
            flash('Profile updated successfully!', 'success')
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error updating database: {str(e)}")
            flash('Failed to update profile. Please try again.', 'danger')

        return redirect(url_for('profile_routes.profile', user_id=user.id))

    return render_template('profile/profile.html', user=user)

def save_file(file):
    """Save the uploaded file and return the filename."""
    upload_folder = 'static/user'
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)

    if file.filename == '':
        logger.warning("No selected file")
        return None

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        # Append timestamp to the filename to prevent overwriting
        base, ext = os.path.splitext(filename)
        timestamp = int(time.time())
        new_filename = f"{base}_{timestamp}{ext}"
        file_path = os.path.join(upload_folder, new_filename)

        try:
            file.save(file_path)
            logger.info(f"File saved to {file_path}")
            return f'user/{new_filename}'
        except Exception as e:
            logger.error(f"Error saving file: {e}")
            return None
    else:
        logger.warning("File type not allowed")
        return None

@profileRoutes.route('/password_reset', methods=['GET', 'POST'])
def password_reset():
    if request.method == 'POST':
        email = request.form['email']
        user = User.query.filter_by(email=email).first()  # Check if the user exists

        if user:
            # Generate a password reset token and send an email
            token = s.dumps(email, salt='password-reset-salt')
            reset_link = url_for('profile_routes.reset_with_token', token=token, _external=True)

            # Send the password reset email
            msg = Message('Password Reset Request', sender='your_email@example.com', recipients=[email])
            msg.body = f'Click the link to reset your password: {reset_link}'
            mail.send(msg)

            # Flash a success message
            flash('We have sent you an email. Please check your inbox.', 'success')
            return redirect(url_for('profile_routes.password_reset'))
        else:
            flash('Email address not found.', 'danger')

    return render_template('profile/password_reset.html')

@profileRoutes.route('/reset/<token>', methods=['GET', 'POST'])
def reset_with_token(token):
    try:
        email = s.loads(token, salt='password-reset-salt', max_age=3600)  # Link valid for 1 hour
    except Exception:
        flash('The reset link is invalid or has expired.', 'danger')
        return redirect(url_for('profile_routes.password_reset'))

    if request.method == 'POST':
        new_password = request.form['new_password']
        user = User.query.filter_by(email=email).first()
        if user:
            user.set_password(new_password)  # Set the new password
            db.session.commit()
            flash('Your password has been updated!', 'success')
            return redirect(url_for('user_routes.login'))  # Correctly redirect to the login page

    return render_template('profile/reset_password.html', token=token)