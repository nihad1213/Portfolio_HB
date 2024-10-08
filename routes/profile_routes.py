#!/usr/bin/env python3

from flask import Blueprint, render_template, request, flash, redirect, url_for
from models.User import User, db
import os
from werkzeug.utils import secure_filename
import logging

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
            logger.debug(f"File received: {file.filename}")
            
            if file and file.filename != '' and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_path = os.path.join(UPLOAD_FOLDER, filename)
                
                try:
                    if not os.path.exists(UPLOAD_FOLDER):
                        os.makedirs(UPLOAD_FOLDER)
                    
                    file.save(file_path)
                    logger.info(f"File saved to: {file_path}")
                    
                    # Update user's profile image
                    user.profile_image = f'user/{filename}'
                    logger.info(f"User profile image updated to: {user.profile_image}")
                except Exception as e:
                    logger.error(f"Error saving file: {str(e)}")
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

    return render_template('profile.html', user=user)

def save_file(file):
    """Save the uploaded file and return the filename."""
    upload_folder = 'static/user'
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)

    if file.filename == '':
        print("No selected file")
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
            print(f"File saved to {file_path}")
            return f'user/{new_filename}'
        except Exception as e:
            print(f"Error saving file: {e}")
            return None
    else:
        print("File type not allowed")
        return None