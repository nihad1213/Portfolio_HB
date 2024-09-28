#!/usr/bin/python3
from sqlalchemy import Column, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from models.BaseModel import BaseModel

class Ticket(BaseModel):
    __tablename__ = 'tickets'

    description = Column(String(255), nullable=True)
    registration = Column(Boolean, default=False)

    event_id = Column(String(36), ForeignKey('events.id'), nullable=False)
    event = relationship('Event', backref='tickets')

    def __init__(self, description=None, registration=False, event=None):
        self.description = description
        self.registration = registration
        self.event = event

    def __repr__(self):
        return f"<Ticket(description='{self.description}', registration={self.registration}, event='{self.event.title}')>"
