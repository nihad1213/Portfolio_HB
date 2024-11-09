from flask import jsonify, session, redirect, url_for, flash, Blueprint, render_template
# Import the models directly from their files
from models.Event import Event 
from models.Like import Like
from models.SavedEvent import SavedEvent
from db import db
import logging
import traceback  # Add this for detailed error tracking

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
            db.session.delete(existing_save)  # Remove save if it already exists
            is_saved = False
        else:
            new_save = SavedEvent(user_id=user_id, event_id=event_id)
            db.session.add(new_save)  # Add save to the database
            is_saved = True

        db.session.commit()

        # Count the number of users who saved the event
        saved_count = SavedEvent.query.filter_by(event_id=event_id).count()
        event.saved_by = saved_count  # Update the event's saved count
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
    # Get the user_id from the session
    user_id = session.get('user_id')

    # If the user is not logged in (i.e., user_id is not in session), redirect to login
    if not user_id:
        return redirect(url_for('user_routes.login'))

    # Get the saved events by the user (using the user_id from the session)
    saved_events = db.session.query(Event).join(SavedEvent, SavedEvent.event_id == Event.id).filter(SavedEvent.user_id == user_id).all()

    # Pass the saved events to the template
    return render_template('main/saved_events.html', events=saved_events)