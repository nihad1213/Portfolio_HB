#!/usr/bin/env python3

#!/usr/bin/env python3

from flask import Blueprint, render_template, request, flash, redirect, session, url_for
from werkzeug.security import generate_password_hash
from models.User import User 
from models.BaseModel import db
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity

userRoutes = Blueprint('user_routes', __name__)

@userRoutes.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = request.form.get('user')
        password = request.form.get('password')

        if not user or not password:
            flash('Please fill out both fields', 'error-login')
            return render_template('user/login.html')

        user_obj = User.find_by_email(user) or User.find_by_username(user)

        if user_obj and user_obj.check_password(password):
            session['user_id'] = user_obj.id
            flash('Logged in successfully!', 'success-login')
            return redirect(url_for('index'))
        else:
            flash('Username/Email or password is incorrect', 'error-login')

    return render_template('user/login.html')

@userRoutes.route('/register', methods=['POST'])
def register():
    name = request.form.get('name')
    surname = request.form.get('surname')
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm_password')

    if not name or not surname or not username or not email or not password or not confirm_password:
        flash('Please fill out all fields', 'error-register')
        return redirect(url_for('user_routes.login'))

    if len(password) < 5:
        flash('Password must be at least 5 characters long', 'error-register')
        return redirect(url_for('user_routes.login'))

    if password != confirm_password:
        flash('Passwords do not match', 'error-register')
        return redirect(url_for('user_routes.login'))

    existing_user = User.query.filter((User.email == email) | (User.username == username)).first()
    if existing_user:
        flash('Email or username is already registered', 'error-register')
        return redirect(url_for('user_routes.login'))

    new_user = User(
        name=name,
        surname=surname,
        username=username,
        email=email,
        password=password
    )

    db.session.add(new_user)
    db.session.commit()

    flash('Account created successfully!', 'success-register')
    return redirect(url_for('user_routes.login'))

@userRoutes.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('You have been logged out.', 'success')
    return redirect(url_for('index'))
