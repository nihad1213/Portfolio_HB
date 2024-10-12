#!/usr/bin/python3

from flask import Blueprint, render_template, request, flash, redirect, url_for
from models.Admin import Admin  # Import your Admin model
from db import db  # Import your database session

# Create blueprint
adminRoutes = Blueprint('admin_routes', __name__)

@adminRoutes.route('/admin', methods=['GET', 'POST'])
def admin_index():
    if request.method == 'POST':
        username = request.form.get('adminName')
        email = request.form.get('adminEmail')
        password = request.form.get('adminPassword')
        
        # Check if an admin with the provided username and email exists
        admin = db.session.query(Admin).filter_by(username=username, email=email).first()
        
        if admin and admin.check_password(password):
            # If the admin exists and the password matches, redirect to dashboard
            return redirect(url_for('admin_routes.dashboard'))  # Use the correct endpoint here
        else:
            # If not, flash an error message
            flash('Invalid username, email, or password. Please try again.', 'danger')
            return redirect(url_for('admin_routes.admin_index'))  # Redirect back to login

    return render_template('admin/admin.index.html')

@adminRoutes.route('/admin-dashboard')
def dashboard():
    return render_template('admin/dashboard.html')  # Adjust the template path as needed
