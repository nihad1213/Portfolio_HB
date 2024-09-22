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
    return render_template('festivals.html', current_year=get_current_year())

@footerRoutes.route('/concerts')
def concerts():
    return render_template('concerts.html', current_year=get_current_year())

@footerRoutes.route('/cultural')
def cultural():
    return render_template('cultural.html', current_year=get_current_year())

@footerRoutes.route('/workshops')
def workshops():
    return render_template('workshops.html', current_year=get_current_year())

@footerRoutes.route('/about-us')
def about():
    return render_template('about-us.html', current_year=get_current_year())

@footerRoutes.route('/story')
def story():
    return render_template('story.html', current_year=get_current_year())

@footerRoutes.route('/contact-us')
def contact():
    return render_template('contact-us.html', current_year=get_current_year())

@footerRoutes.route('/faqs')
def faqs():
    return render_template('faqs.html', current_year=get_current_year())

@footerRoutes.route('/submit-contact', methods=['POST'])
def submit_contact():
    name = request.form['name']
    email = request.form['email']
    message = request.form['message']

    # Fetch email username and default sender from environment
    sender_email = current_app.config['MAIL_USERNAME']  # This is your Gmail account
    default_sender = 'nihadnemetli9900@gmail.com'  # Set this to the email you want to display as the sender

    # Create email message
    msg = Message(
        subject=f"New Message From {name}",
        sender=default_sender,  # Set the sender to the desired email
        recipients=[sender_email],  # This is where the email is sent (your Gmail)
        reply_to=email  # Replies will go to the user's email
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