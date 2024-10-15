#!/usr/bin/python3

from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app
from flask_mail import Message, Mail
from models.Admin import Admin
from models.Subscriber import Subscribers
from db import db

# Create blueprint
adminRoutes = Blueprint('admin_routes', __name__)

# Intialze mail
mail = Mail()

# Get admin login part
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
            return redirect(url_for('admin_routes.dashboard'))
        else:
            # If not, flash an error message
            flash('Invalid username, email, or password. Please try again.', 'danger')
            return redirect(url_for('admin_routes.admin_index'))

    return render_template('admin/admin.index.html')

# Get dashboard
@adminRoutes.route('/admin-dashboard')
def dashboard():
    return render_template('admin/dashboard.html')

# Admin Routes

# Route to handle adding a new admin
@adminRoutes.route('/admin/add', methods=['POST'])
def add_admin():
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    
    # Check if admin with the same username or email already exists
    existing_admin = Admin.query.filter((Admin.username == username) | (Admin.email == email)).first()
    if existing_admin:
        flash('Admin with that username or email already exists!', 'danger')
        return redirect(url_for('admin_routes.admin_list'))
    
    # Create and add the new admin
    new_admin = Admin(username=username, email=email, password=password)
    db.session.add(new_admin)
    db.session.commit()
    flash('Admin added successfully!', 'success')
    
    return redirect(url_for('admin_routes.admin_list'))

# Display all admins and allow adding a new admin
@adminRoutes.route('/admins', methods=['GET', 'POST'])
def admin_list():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        new_admin = Admin(username=username, email=email, password=password)
        db.session.add(new_admin)
        db.session.commit()
        flash('Admin added successfully!', 'success')
        return redirect(url_for('admin_routes.admin_list'))
    
    admins = Admin.query.all()
    return render_template('admin/admins.html', admins=admins)

# Edit admin
@adminRoutes.route('/admin/edit/<string:admin_id>', methods=['GET', 'POST'])
def edit_admin(admin_id):
    admin = Admin.query.get(admin_id)
    
    if not admin:
        flash('Admin not found!', 'danger')
        return redirect(url_for('admin_routes.admin_list'))

    if request.method == 'POST':
        # Update the username and email
        admin.username = request.form['username']
        admin.email = request.form['email']

        # Check if a new password was provided
        new_password = request.form.get('password')
        if new_password:
            admin.set_password(new_password)
        
        db.session.commit()
        flash('Admin updated successfully!', 'success')
        return redirect(url_for('admin_routes.admin_list'))

    return render_template('admin/edit-admin.html', admin=admin)

# Delete admin confirmation page
@adminRoutes.route('/admin/delete/<string:admin_id>', methods=['GET'])
def delete_admin(admin_id):
    admin = Admin.query.get(admin_id)
    return render_template('admin/delete-admin.html', admin=admin)

# Confirm admin deletion
@adminRoutes.route('/admin/delete/<string:admin_id>', methods=['POST'])
def confirm_delete_admin(admin_id):
    admin = Admin.query.get(admin_id)
    db.session.delete(admin)
    db.session.commit()
    flash('Admin deleted successfully!', 'success')
    return redirect(url_for('admin_routes.admin_list'))

# Send message to subscribers
@adminRoutes.route('/send-message', methods=['GET', 'POST'])
def send_message():
    if request.method == 'POST':
        subject = request.form['subject']
        message = request.form['message']
        
        default_sender = current_app.config['MAIL_DEFAULT_SENDER']
        subscribers = db.session.query(Subscribers).all()

        if not subscribers:
            flash('No subscribers found!', 'warning')
            return redirect(url_for('admin_routes.send_message'))

        for subscriber in subscribers:
            msg = Message(
                subject=subject,
                sender=default_sender,
                recipients=[subscriber.email]
            )
            msg.body = f"{message}\n\nThank you for your attention!"

            try:
                mail.send(msg)
                flash(f'Email sent to {subscriber.email}', 'success')
            except Exception as e:
                flash(f'Error sending message to {subscriber.email}: {e}', 'danger')

        return redirect(url_for('admin_routes.send_message'))

    return render_template('admin/send-message.html')