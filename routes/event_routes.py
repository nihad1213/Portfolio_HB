from flask import jsonify, session, redirect, url_for, flash, Blueprint, render_template
from models.Event import Event 
from models.Like import Like
from models.User import User
from models.Attendance import Attendance
from models.SavedEvent import SavedEvent
from db import db
import logging
import traceback
import smtplib
import io
from reportlab.pdfgen import canvas
from dotenv import load_dotenv
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from reportlab.pdfgen import canvas 

load_dotenv()

MAIL_SERVER = os.getenv('MAIL_SERVER')
MAIL_PORT = os.getenv('MAIL_PORT')
MAIL_USE_TLS = os.getenv('MAIL_USE_TLS') == 'True'
MAIL_USERNAME = os.getenv('MAIL_USERNAME')
MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER')

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

event_routes = Blueprint('event_routes', __name__)

@event_routes.route('/like_event/<string:event_id>', methods=['POST'])
def like_event(event_id):
    try:
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({
                "success": False,
                "message": "Please log in to like the event"
            }), 403

        event = Event.query.get(event_id)
        if not event:
            return jsonify({
                "success": False,
                "message": "Event not found"
            }), 404

        existing_like = Like.query.filter_by(user_id=user_id, event_id=event_id).first()
        
        if existing_like:
            db.session.delete(existing_like)
            is_liked = False
        else:
            new_like = Like(user_id=user_id, event_id=event_id)
            db.session.add(new_like)
            is_liked = True
        
        db.session.commit()
        
        like_count = Like.query.filter_by(event_id=event_id).count()
        event.likes = like_count
        db.session.commit()

        return jsonify({
            "success": True,
            "likes": like_count,
            "is_liked": is_liked
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({
            "success": False,
            "message": "An error occurred"
        }), 500

@event_routes.route('/save_event/<string:event_id>', methods=['POST'])
def save_event(event_id):
    try:
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({
                "success": False,
                "message": "Please log in to save the event"
            }), 403  # User must be logged in to save events

        event = Event.query.get(event_id)
        if not event:
            return jsonify({
                "success": False,
                "message": "Event not found"
            }), 404  # Event not found

        existing_save = SavedEvent.query.filter_by(user_id=user_id, event_id=event_id).first()

        if existing_save:
            db.session.delete(existing_save)
            is_saved = False
        else:
            new_save = SavedEvent(user_id=user_id, event_id=event_id)
            db.session.add(new_save)
            is_saved = True

        db.session.commit()

        saved_count = SavedEvent.query.filter_by(event_id=event_id).count()
        event.saved_by = saved_count
        db.session.commit()

        return jsonify({
            "success": True,
            "saved_count": saved_count,
            "is_saved": is_saved
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({
            "success": False,
            "message": "An error occurred"
        }), 500
    
@event_routes.route('/saved-events')
def saved_events():
    user_id = session.get('user_id')

    if not user_id:
        return redirect(url_for('user_routes.login'))

    saved_events = db.session.query(Event).join(SavedEvent, SavedEvent.event_id == Event.id).filter(SavedEvent.user_id == user_id).all()

    return render_template('main/saved_events.html', events=saved_events)

@event_routes.route('/attend_event/<string:event_id>', methods=['POST'])
def attend_event(event_id):
    try:
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({
                "success": False,
                "message": "Please log in to attend the event"
            }), 403

        event = Event.query.get(event_id)
        if not event:
            return jsonify({
                "success": False,
                "message": "Event not found"
            }), 404

        existing_attendance = Attendance.query.filter_by(user_id=user_id, event_id=event_id).first()
        if existing_attendance:
            return jsonify({
                "success": False,
                "message": "You have already attended this event"
            }), 400

        if event.capacity <= 0:
            return jsonify({
                "success": False,
                "message": "Event is full"
            }), 400

        new_attendance = Attendance(user_id=user_id, event_id=event_id)
        db.session.add(new_attendance)
        db.session.commit()

        event.capacity -= 1
        event.attendees += 1
        db.session.commit()

        user = User.query.get(user_id)

        send_attendance_email(user.email, event)

        return jsonify({
            "success": True,
            "message": "You have successfully attended the event"
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({
            "success": False,
            "message": "An error occurred"
        }), 500


def send_attendance_email(user_email, event):
    # Create the email
    msg = MIMEMultipart()
    msg['From'] = MAIL_DEFAULT_SENDER
    msg['To'] = user_email
    msg['Subject'] = f'Confirmation of Attendance for {event.title}'

    body = f"""
Hello,

You have successfully attended the event: {event.title}. We look forward to seeing you there!

Best regards,
AzerbaijanFest Team
"""
    msg.attach(MIMEText(body, 'plain'))

    # Create the PDF with a more vibrant and modern design
    pdf_io = io.BytesIO()
    c = canvas.Canvas(pdf_io)

    # Add a gradient-like background effect
    c.setFillColorRGB(0.9, 0.95, 1)  # Light blue background
    c.rect(0, 0, 600, 850, fill=True, stroke=False)

    # Add a large, bold header with branding
    c.setFont("Helvetica-Bold", 28)
    c.setFillColorRGB(0.1, 0.3, 0.8)  # Deep blue for branding
    c.drawCentredString(300, 800, "AzerbaijanFest Attendance Confirmation")

    # Add a subtle line under the header
    c.setStrokeColorRGB(0.1, 0.3, 0.8)  # Match branding blue
    c.setLineWidth(2)
    c.line(50, 790, 550, 790)

    # Add event details in an elegant layout
    c.setFont("Helvetica", 16)
    c.setFillColorRGB(0, 0, 0)  # Black text
    c.drawString(80, 750, f"Event: {event.title}")
    c.drawString(80, 720, f"Date: {event.date.strftime('%Y-%m-%d %H:%M')}")
    c.drawString(80, 690, f"Location: {event.location}")

    # Add a decorative "Thank You" message in the center
    c.setFont("Helvetica-Bold", 22)
    c.setFillColorRGB(0.2, 0.7, 0.3)  # Bright green
    c.drawCentredString(300, 640, "Thank you for joining us!")

    # Add AzerbaijanFest branding at the bottom
    c.setFont("Helvetica-Oblique", 14)
    c.setFillColorRGB(0.6, 0.2, 0.7)  # Purple for branding contrast
    c.drawCentredString(300, 120, "With love, AzerbaijanFest Team")

    # Add decorative elements (optional logo)
    c.setFont("Helvetica", 12)
    c.setFillColorRGB(0.5, 0.5, 0.5)  # Subtle gray for details
    c.drawCentredString(300, 100, "Visit us at www.azerbaijanfest.com")
    
    # Add a colorful footer bar
    c.setFillColorRGB(0.1, 0.3, 0.8)  # Deep blue
    c.rect(0, 50, 600, 30, fill=True, stroke=False)

    # Add white text over the footer
    c.setFont("Helvetica-Bold", 12)
    c.setFillColorRGB(1, 1, 1)  # White
    c.drawCentredString(300, 60, "Thank you for being a part of AzerbaijanFest!")

    c.save()

    # Attach PDF to email
    pdf_io.seek(0)
    part = MIMEBase('application', 'octet-stream')
    part.set_payload(pdf_io.read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', 'attachment', filename=f'{event.title}_attendance.pdf')
    msg.attach(part)

    # Send email via SMTP
    try:
        with smtplib.SMTP(MAIL_SERVER, MAIL_PORT) as server:
            server.starttls()  # Start TLS encryption
            server.login(MAIL_USERNAME, MAIL_PASSWORD)  # Login with your email credentials
            server.send_message(msg)
    except Exception as e:
        print(f'Error sending email: {e}')
