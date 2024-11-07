#!/usr/bin/env python3

import os
from flask import Blueprint, render_template, request, redirect, flash, url_for
from werkzeug.utils import secure_filename
from models.Event import Event
from models.Admin import Admin
from models.Category import Category
from models.Subscriber import Subscribers
from db import db
from flask_mail import Message, Mail
from flask import flash

mail = Mail()

# Allowed image files
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Path for images
UPLOAD_FOLDER = 'static/event'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Create blueprint
mainRoutes = Blueprint('main_routes', __name__)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@mainRoutes.route('/create-event', methods=['GET', 'POST'])
def create_event():
    if request.method == 'POST':
        # Get form data
        event_name = request.form.get('eventName')
        event_description = request.form.get('eventDescription')
        event_date = request.form.get('eventDate')
        event_time = request.form.get('eventTime')
        event_location = request.form.get('eventLocation')
        event_category = request.form.get('eventCategory')
        attendees_number = request.form.get('attendeesNumber')

        # Handle image upload
        file = request.files.get('eventImage')
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            image_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(image_path)
        else:
            flash("Invalid image format. Please upload PNG, JPG, JPEG, or GIF.", "error")
            return redirect(request.url)

        # Save event in the database (status is set to inactive by default)
        try:
            category = Category.query.filter_by(id=event_category).first()
            new_event = Event(
                title=event_name,
                date=f"{event_date} {event_time}",
                location=event_location,
                category=category,
                image=filename,
                description=event_description,
                status=False,  # Default inactive status
                capacity=int(attendees_number)
            )
            db.session.add(new_event)
            db.session.commit()

            # Fetch admins to send notification
            admins = Admin.query.all()

            for admin in admins:
                # Create the email content
                msg = Message(
                    subject="New Event Waiting for Approval",
                    recipients=[admin.email],
                    body=f"A new event '{event_name}' has been created and is awaiting approval. Please review it in the admin panel."
                )
                try:
                    # Send email to each admin
                    mail.send(msg)
                except Exception as e:
                    flash(f"Error sending email: {e}", "error")
                    break

            flash("Event created successfully! Waiting for admin approval.", "create-event-success")
        except Exception as e:
            db.session.rollback()
            flash(f"Error creating event: {e}", "error")
        
        return redirect(url_for('main_routes.events'))

    categories = Category.query.all()
    return render_template('main/create-event.html', categories=categories)

@mainRoutes.route('/events')
def events():
    events = Event.query.filter_by(status=True).all()
    return render_template('main/events.html', events=events)

@mainRoutes.route('/event/<uuid:event_id>')
def event_details(event_id):
    event = Event.query.get_or_404(event_id)
    return render_template('main/event-details.html', event=event)

# Route to attend the event
@mainRoutes.route('/event/<uuid:event_id>/attend', methods=['POST'])
def attend_event(event_id):
    event = Event.query.get_or_404(event_id)
    try:
        event.attendees += 1
        db.session.commit()
        flash("You have successfully attended this event!", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Error attending event: {e}", "error")
    
    return redirect(url_for('main_routes.event_details', event_id=event_id))

# Route to like the event
@mainRoutes.route('/event/<uuid:event_id>/like', methods=['POST'])
def like_event(event_id):
    event = Event.query.get_or_404(event_id)
    try:
        event.likes += 1
        db.session.commit()
        flash("You have liked this event!", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Error liking event: {e}", "error")
    
    return redirect(url_for('main_routes.event_details', event_id=event_id))

@mainRoutes.route('/subscribe', methods=['POST'])
def subscribe():
    email = request.form.get('email')
    
    if not email:
        return '''<script>
                    alert("Email is required!");
                    window.location.href = document.referrer;
                  </script>'''

    # Check if email already exists in the database
    existing_subscriber = Subscribers.query.filter_by(email=email).first()

    if existing_subscriber:
        return '''<script>
                    alert("This email is already subscribed!");
                    window.location.href = document.referrer;
                  </script>'''

    # Add new subscriber
    new_subscriber = Subscribers(email=email)
    try:
        new_subscriber.save()
        return '''<script>
                    alert("Successfully subscribed!");
                    window.location.href = document.referrer;
                  </script>'''
    except Exception as e:
        print(f"Error: {e}")
        return '''<script>
                    alert("There was an issue adding your email!");
                    window.location.href = document.referrer;
                  </script>'''

