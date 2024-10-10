#!/usr/bin/env python3

from flask import Blueprint, render_template, request, redirect, flash
from models.Subscriber import Subscribers

# Create blueprint
mainRoutes = Blueprint('main_routes', __name__)

@mainRoutes.route('/create-event')
def create_event():
    return render_template('main/create-event.html')

@mainRoutes.route('/events')
def events():
    return render_template('main/events.html')

@mainRoutes.route('/subscribe', methods=['POST'])
def subscribe():
    email = request.form.get('email')
    
    if not email:
        flash("Email is required!", "error")
        return redirect(request.referrer)

    # Check if email already exists in the database
    existing_subscriber = Subscribers.query.filter_by(email=email).first()

    if existing_subscriber:
        flash("This email is already subscribed!", "warning")
        return redirect(request.referrer)

    # Add new subscriber
    new_subscriber = Subscribers(email=email)
    try:
        new_subscriber.save()
        flash("Successfully subscribed!", "success")
    except Exception as e:
        flash("There was an issue adding your email!", "error")
        print(f"Error: {e}")
    
    return redirect(request.referrer)