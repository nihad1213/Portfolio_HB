#!/usr/bin/env python3

<<<<<<< HEAD
from flask import Blueprint, render_template, request, flash, redirect, session, url_for, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from models.User import User  # Correctly import User
from models.BaseModel import db  # Correctly import db
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from datetime import timedelta
=======
#!/usr/bin/env python3

from flask import Blueprint, render_template, request, flash, redirect, session, url_for
from werkzeug.security import generate_password_hash
from models.User import User 
from models.BaseModel import db
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
>>>>>>> origin/main

# Initialize Blueprints
userRoutes = Blueprint('user_routes', __name__)
<<<<<<< HEAD
dashboardRoutes = Blueprint('dashboard_routes', __name__)
=======
>>>>>>> origin/main

@userRoutes.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = request.form.get('user')
        password = request.form.get('password')

        if not user or not password:
            flash('Please fill out both fields', 'error')
            return render_template('login.html')

<<<<<<< HEAD
        user = User.find_by_email(email)  # Use the class method to find the user

        if user and user.check_password(password):  # Use the check_password method
            # Create JWT token
            access_token = create_access_token(identity=user.id, expires_delta=timedelta(hours=1))
            session['access_token'] = access_token

            flash('Logged in successfully!', 'success')
            return redirect(url_for('dashboard_routes.dashboard'))  # Change to redirect to main page here
=======
        user_obj = User.find_by_email(user) or User.find_by_username(user)
        
        if user_obj and user_obj.check_password(password):
            session['user_id'] = user_obj.id
            flash('Logged in successfully!', 'success')
            return redirect(url_for('index'))
>>>>>>> origin/main
        else:
            flash('Username/Email or password is incorrect', 'error')

    return render_template('login.html')

@userRoutes.route('/register', methods=['POST'])
def register():
<<<<<<< HEAD
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
=======
    name = request.form.get('name')
    surname = request.form.get('surname')
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm_password')

    if not name or not surname or not username or not email or not password or not confirm_password:
        flash('Please fill out all fields', 'error')
        return redirect(url_for('user_routes.login'))

    if password != confirm_password:
        flash('Passwords do not match', 'error')
        return redirect(url_for('user_routes.login'))

    existing_user = User.query.filter((User.email == email) | (User.username == username)).first()
    if existing_user:
        flash('Email or username is already registered', 'error')
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

    flash('Account created successfully!', 'success')
    return redirect(url_for('user_routes.login'))
>>>>>>> origin/main

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
<<<<<<< HEAD
=======

@userRoutes.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('You have been logged out.', 'success')
    return redirect(url_for('index'))
>>>>>>> origin/main
