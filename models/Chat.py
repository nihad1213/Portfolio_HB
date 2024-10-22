#!/usr/bin/python3
from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from models.BaseModel import BaseModel, db

class Chat(BaseModel, db.Model):  # Inherit from db.Model to integrate with SQLAlchemy ORM
    __tablename__ = 'chats'

    id = db.Column(db.String(36), primary_key=True)  # Match type with User's id
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)  # ForeignKey should refer to the correct column
    message = db.Column(String(255), nullable=False)
    created_at = db.Column(DateTime, default=datetime.utcnow)  # Add timestamp for chat creation

    # Define the relationship between Chat and User, lazy='dynamic' to improve query performance
    user = relationship('User', backref='chats')

    def __init__(self, user_id, message):
        self.user_id = user_id
        self.message = message

    def __repr__(self):
        return f"<Chat(user_id='{self.user_id}', message='{self.message}', created_at='{self.created_at}')>"
