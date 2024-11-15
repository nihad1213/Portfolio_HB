#!/usr/bin/python3

from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app, session
from flask_mail import Message, Mail
from models.Admin import Admin
from models.Subscriber import Subscribers
from models.Category import Category
from models.Event import Event
from models.User import User
from db import db
from werkzeug.utils import secure_filename
import os

# Create blueprint
adminRoutes = Blueprint('admin_routes', __name__)

# Intialze mail
mail = Mail()

# Define allowed image extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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
            # If the admin exists and the password matches, store their ID in session
            session['admin_username'] = admin.username
            return redirect(url_for('admin_routes.dashboard'))
        else:
            # If not, flash an error message
            flash('Invalid username, email, or password. Please try again.', 'danger')
            return redirect(url_for('admin_routes.admin_index'))

    return render_template('admin/admin.index.html')

# Get dashboard
@adminRoutes.route('/admin-dashboard')
def dashboard():
    # Retrieve the logged-in admin's username from session
    username = session.get('admin_username', "Admin")

    total_users = User.query.count()
    active_sessions = 0 
    
    pending_tasks = Event.query.filter_by(status=False).count() 
    
    total_subscribers = Subscribers.query.count()

    # Pass the data to the template
    return render_template('admin/dashboard.html', 
                           username=username,
                           total_users=total_users,
                           active_sessions=active_sessions,
                           pending_tasks=pending_tasks,
                           total_subscribers=total_subscribers)


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
    # Handle form submission to add a new admin
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        new_admin = Admin(username=username, email=email, password=password)
        db.session.add(new_admin)
        db.session.commit()
        flash('Admin added successfully!', 'success')
        return redirect(url_for('admin_routes.admin_list'))
    
    # Get search query and page number from request
    search_query = request.args.get('search', '')
    page = request.args.get('page', 1, type=int)
    
    query = Admin.query
    if search_query:
        query = query.filter(
            (Admin.username.ilike(f'%{search_query}%')) |
            (Admin.email.ilike(f'%{search_query}%'))
        )
    
    per_page = 7
    admins = query.paginate(page=page, per_page=per_page, error_out=False)
    
    total_pages = admins.pages
    
    return render_template(
        'admin/admins.html', 
        admins=admins.items,
        page=page, 
        total_pages=total_pages,
        search_query=search_query
    )

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

# Add Category
@adminRoutes.route('/categories/add', methods=['GET', 'POST'])
def add_category():
    if request.method == 'POST':
        name = request.form['name']
        file = request.files['category_image']
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            image_path = os.path.join('static/category', filename)
            file.save(image_path)
            
            # Create the category
            new_category = Category(name=name, category_image=filename)
            db.session.add(new_category)
            db.session.commit()
            
            flash('Category added successfully with image!', 'success')
        else:
            flash('Invalid image format or no image uploaded! Allowed types: png, jpg, jpeg, gif.', 'danger')
        
        return redirect(url_for('admin_routes.list_categories'))
    
    return render_template('admin/add-category.html')

# List Categories Route
@adminRoutes.route('/categories', methods=['GET'])
def list_categories():
    # Get search query and page number from the request
    search_query = request.args.get('search', '')
    page = request.args.get('page', 1, type=int)

    query = Category.query
    if search_query:
        query = query.filter(Category.name.ilike(f'%{search_query}%'))

    
    per_page = 5
    categories = query.paginate(page=page, per_page=per_page, error_out=False)

    total_pages = categories.pages

    return render_template(
        'admin/categories.html',
        categories=categories.items,
        page=page,
        total_pages=total_pages,
        search_query=search_query
    )

# Edit Category Route
@adminRoutes.route('/categories/edit/<string:category_id>', methods=['GET', 'POST'])
def edit_category(category_id):
    category = Category.query.get(category_id)
    
    if not category:
        flash('Category not found!', 'danger')
        return redirect(url_for('admin_routes.list_categories'))
    
    if request.method == 'POST':
        category.name = request.form['name']
        file = request.files['category_image']

        # If a new file is uploaded
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            image_path = os.path.join('static/category', filename)
            file.save(image_path)
            category.category_image = filename
        
        db.session.commit()
        flash('Category updated successfully!', 'success')
        return redirect(url_for('admin_routes.list_categories'))
    
    return render_template('admin/edit-category.html', category=category)

# Delete Category Route
@adminRoutes.route('/categories/delete/<uuid:category_id>', methods=['GET', 'POST'])
def delete_category(category_id):
    category = Category.query.get(category_id)
    
    if request.method == 'POST':
        if category:
            db.session.delete(category)
            db.session.commit()
            flash('Category deleted successfully!', 'success')
        else:
            flash('Category not found!', 'danger')
        
        return redirect(url_for('admin_routes.list_categories'))

    return render_template('admin/delete-category.html', category=category)

# Route to list all events
@adminRoutes.route('/admin/events')
def admin_events():
    search_query = request.args.get('search', '')
    page = request.args.get('page', 1, type=int)
    
    query = Event.query
    if search_query:
        query = query.filter(Event.title.ilike(f'%{search_query}%'))
    
    per_page = 10
    events = query.paginate(page=page, per_page=per_page, error_out=False)
    
    total_pages = events.pages
    
    return render_template(
        'admin/events.html', 
        events=events.items,
        page=page, 
        total_pages=total_pages,
        search_query=search_query
    )

# Route to display event details
@adminRoutes.route('/admin/event/<uuid:event_id>')
def admin_event_details(event_id):
    event = Event.query.get_or_404(event_id)
    return render_template('admin/event_details.html', event=event)

# Route to toggle event status (Active/Inactive)
@adminRoutes.route('/admin/event/toggle-status/<uuid:event_id>', methods=['POST'])
def toggle_event_status(event_id):
    event = Event.query.get_or_404(event_id)
    event.status = not event.status
    db.session.commit()
    flash(f"Event '{event.title}' status updated to {'active' if event.status else 'inactive'}", 'success')
    return redirect(url_for('admin_routes.admin_events'))