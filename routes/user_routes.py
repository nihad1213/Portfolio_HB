#!/usr/bin/env python3

from flask import Blueprint, render_template, request, flash, redirect, session, url_for, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from models.User import User  # Correctly import User
from models.BaseModel import db  # Correctly import db
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from datetime import timedelta

# Initialize Blueprints
userRoutes = Blueprint('user_routes', __name__)
dashboardRoutes = Blueprint('dashboard_routes', __name__)

@userRoutes.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # Validate input
        if not email or not password:
            flash('Please fill out both fields', 'error')
            return render_template('login.html')

        user = User.find_by_email(email)  # Use the class method to find the user

        if user and user.check_password(password):  # Use the check_password method
            # Create JWT token
            access_token = create_access_token(identity=user.id, expires_delta=timedelta(hours=1))
            session['access_token'] = access_token

            flash('Logged in successfully!', 'success')
            return redirect(url_for('dashboard_routes.dashboard'))  # Change to redirect to main page here
        else:
            flash('Email or password is incorrect', 'error')

    return render_template('login.html')

@userRoutes.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name').strip()
        surname = request.form.get('surname').strip()
        username = request.form.get('username').strip()
        email = request.form.get('email').strip()
        password = request.form.get('password').strip()
        confirm_password = request.form.get('confirm-password').strip()  # Ensure this is the same name
        
        # Debugging statements
        print(f"Name: {name}")
        print(f"Surname: {surname}")
        print(f"Username: {username}")
        print(f"Email: {email}")
        print(f"Password: {password}")
        print(f"Confirm Password: {confirm_password}")
        
        # Check if all fields are filled
        if not name or not surname or not username or not email or not password or not confirm_password:
            flash('Please fill out all fields', 'error')
            return render_template('register.html')

        # Check if passwords match
        if password != confirm_password:
            flash('Passwords do not match!', 'error')
            return render_template('register.html')

        # Hash the password
        hashed_password = generate_password_hash(password)

        # Create new user instance
        new_user = User(name=name, surname=surname, password=hashed_password, email=email)

        # Save user to the database
        try:
            new_user.save()
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('user_routes.login'))  # Redirect to login page after successful registration
        except Exception as e:
            flash(f'An error occurred: {str(e)}', 'error')

    return render_template('register.html')

@dashboardRoutes.route('/dashboard', methods=['GET'])
@jwt_required()  # Protect this route with JWT
def dashboard():
    current_user_id = get_jwt_identity()

    user = User.query.get(current_user_id)

    if not user:
        flash('User not found', 'error')
        return redirect(url_for('user_routes.login'))

    user_data = {
        'name': user.name,
        'surname': user.surname,
        'email': user.email,
        'attend': user.attend,
        'created_at': user.created_at,
        'updated_at': user.updated_at
    }

    return render_template('dashboard.html', user=user_data)
