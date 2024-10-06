#!/usr/bin/env python3

from flask import Blueprint, render_template, request, flash, redirect, session, url_for, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from models import User 
from models.BaseModel import db  
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from datetime import timedelta
from flask_jwt_extended import create_access_token


userRoutes = Blueprint('user_routes', __name__)


from flask_jwt_extended import create_access_token

@userRoutes.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # Validate input
        if not email or not password:
            flash('Please fill out both fields', 'error')
            return render_template('login.html')

        user = User.find_by_email(email)
        
        if user and user.check_password(password):
            session['user_id'] = user.id
            flash('Logged in successfully!', 'success')
            return redirect(url_for('dashboard_routes.dashboard')) 
        else:
            flash('Email or password is incorrect', 'error')

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
        birth_date = request.form.get('birth_date')

        if not name or not surname or not username or not email or not password or not confirm_password or not birth_date:
            flash('Please fill out all fields', 'error')
            return render_template('register.html')

        if password != confirm_password:
            flash('Passwords do not match', 'error')
            return render_template('register.html')

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email is already registered', 'error')
            return render_template('register.html')

        hashed_password = generate_password_hash(password, method='sha256')

        new_user = User(
            name=name,
            surname=surname,
            username=username,
            email=email,
            password=hashed_password,
            birth_date=birth_date
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