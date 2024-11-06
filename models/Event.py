#!/usr/bin/python3
from sqlalchemy import Column, String, Date, Boolean, ForeignKey, Integer
from sqlalchemy.orm import relationship
from models.BaseModel import BaseModel

class Event(BaseModel):
    __tablename__ = 'events'

    title = Column(String(100), nullable=False)
    date = Column(Date, nullable=False)
    location = Column(String(255), nullable=False)
    category_id = Column(String(36), ForeignKey('categories.id'), nullable=False)
    category = relationship('Category', backref='events')
    image = Column(String(255), nullable=True)
    description = Column(String(255), nullable=True)
    registration = Column(Boolean, default=False)
    status = Column(Boolean, default=False)

    # Fields for tracking likes, attendees, and capacity
    attendees = Column(Integer, default=0)
    likes = Column(Integer, default=0)
    capacity = Column(Integer, nullable=True)

    def __init__(self, title, date, location, category, image=None, description=None, registration=False, status=False, capacity=None):
        self.title = title
        self.date = date
        self.location = location
        self.category = category
        self.image = image
        self.description = description
        self.registration = registration
        self.status = status
        self.capacity = capacity

    def __repr__(self):
        return f"<Event(title='{self.title}', date='{self.date}', location='{self.location}', category='{self.category.name}', status='{self.status}', capacity='{self.capacity}')>"
