from flask import jsonify, session, redirect, url_for, flash, Blueprint
# Import the models directly from their files
from models.Event import Event 
from models.Like import Like
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