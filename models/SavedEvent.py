from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from models.BaseModel import BaseModel
from db import db

class SavedEvent(BaseModel):
    __tablename__ = 'saved_events'

    user_id = Column(String(36), ForeignKey('users.id'), nullable=False)
    event_id = Column(String(36), ForeignKey('events.id'), nullable=False)

    # Relationships
    user = relationship('User', backref='saved_events')
    event = relationship('Event', backref='saved_by_users')

    def __init__(self, user_id, event_id):
        self.user_id = user_id
        self.event_id = event_id
