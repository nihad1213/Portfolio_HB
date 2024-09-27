#!/usr/bin/env python3

from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app
from flask_mail import Mail, Message
from datetime import datetime

# Create blueprint
footerRoutes = Blueprint('footer_routes', __name__)

# Initialize mail (if not already initialized in the main app)
mail = Mail()

# Function to get the current year
def get_current_year():
    return datetime.now().year

# Routes and Functions
@footerRoutes.route('/festivals')
def festivals():
    return render_template('footer-links/festivals.html', current_year=get_current_year())

@footerRoutes.route('/concerts')
def concerts():
    return render_template('footer-links/concerts.html', current_year=get_current_year())

@footerRoutes.route('/cultural')
def cultural():
    return render_template('footer-links/cultural.html', current_year=get_current_year())

@footerRoutes.route('/workshops')
def workshops():
    return render_template('footer-links/workshops.html', current_year=get_current_year())

@footerRoutes.route('/about-us')
def about():
    return render_template('footer-links/about-us.html', current_year=get_current_year())

@footerRoutes.route('/story')
def story():
    return render_template('footer-links/story.html', current_year=get_current_year())

@footerRoutes.route('/contact-us')
def contact():
    return render_template('footer-links/contact-us.html', current_year=get_current_year())

@footerRoutes.route('/faqs')
def faqs():
    return render_template('footer-links/faqs.html', current_year=get_current_year())

@footerRoutes.route('/submit-contact', methods=['POST'])
def submit_contact():
    name = request.form['name']
    email = request.form['email']
    message = request.form['message']

    sender_email = current_app.config['MAIL_USERNAME'] 
    default_sender = current_app.config['MAIL_DEFAULT_SENDER']

    # Create email message
    msg = Message(
        subject=f"New Message From {name}",
        sender=default_sender,
        recipients=[sender_email],
        reply_to=email
    )

    # Set custom headers for the sender information
    msg.headers = {
        'X-Sender-Name': name,
        'X-Sender-Email': email
    }

    # Email body with structured format
    msg.body = (
        f"New Message From: {name}\n"
        f"Sender Email: {email}\n\n"
        f"Message:\n{message}\n\n"
        "Please respond to this email."
    )

    try:
        # Send the email
        mail.send(msg)
        flash('Your message has been sent successfully!', 'success')
        return redirect(url_for('footer_routes.contact'))
    except Exception as e:
        flash(f'Error sending message: {e}', 'danger')
        return redirect(url_for('footer_routes.contact'))