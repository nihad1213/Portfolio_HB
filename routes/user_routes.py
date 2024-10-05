#!/usr/bin/env python3

# Importing Modules
from flask import Blueprint, render_template, request, flash, redirect, session, url_for, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from models.User import User 
from models.BaseModel import db  
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from datetime import timedelta
from datetime import datetime
from flask_jwt_extended import create_access_token


userRoutes = Blueprint('user_routes', __name__)


@userRoutes.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # Query the user by email
        user = User.find_by_email(email)

        # Check if user exists and password matches
        if user and user.check_password(password):
            # Create the access token
            access_token = create_access_token(identity=user.id)
            
            # Store user ID and token in the session
            session['user_id'] = user.id
            session['access_token'] = access_token

            flash('Logged in successfully!', 'success')
            return redirect(url_for('index'))

        else:
            flash('Email or password is incorrect', 'danger')

    return render_template('login.html')





@userRoutes.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        surname = request.form.get('surname')
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        birth_date = request.form.get('birthdate')

        # Check for empty fields
        if not name or not surname or not username or not email or not password or not confirm_password or not birth_date:
            flash('Please fill out all fields', 'danger')
            return render_template('register.html')

        # Check if passwords match
        if password != confirm_password:
            flash('Passwords do not match', 'danger')
            return render_template('register.html')

        # Check if the email is already registered
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email is already registered', 'danger')
            return render_template('register.html')

        # Create and save the new user
        new_user = User(
            name=name,
            surname=surname,
            username=username,
            email=email,
            password=password,
            birth_date=datetime.strptime(birth_date, '%Y-%m-%d')
        )

        db.session.add(new_user)
        db.session.commit()

        flash('Account created successfully!', 'success')
        return redirect(url_for('user_routes.login'))

    return render_template('register.html')


dashboardRoutes = Blueprint('dashboard_routes', __name__)

@dashboardRoutes.route('/dashboard', methods=['GET'])
@jwt_required()
def dashboard():
    current_user_id = get_jwt_identity()

    user = User.query.get(current_user_id)

    if not user:
        flash('User not found', 'danger')
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