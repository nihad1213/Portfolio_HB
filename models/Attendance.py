#!/usr/bin/python3
from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from models.BaseModel import BaseModel

class Attendance(BaseModel):
    __tablename__ = 'attendances'

    user_id = Column(String(36), ForeignKey('users.id'), nullable=False)
    event_id = Column(String(36), ForeignKey('events.id'), nullable=False)

    user = relationship('User', backref='attendances')
    event = relationship('Event', backref='attendances')

    def __init__(self, user_id, event_id):
        self.user_id = user_id
        self.event_id = event_id

    def __repr__(self):
        return f"<Attendance(user_id='{self.user_id}', event_id='{self.event_id}')>"
