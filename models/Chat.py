#!/usr/bin/python3
from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from models.BaseModel import BaseModel
from datetime import datetime

class Chat(BaseModel):
    __tablename__ = 'chats'

    user_id = Column(String(36), ForeignKey('users.id'), nullable=False)
    message = Column(String(255), nullable=False)

    user = relationship('User', backref='chats')

    def __init__(self, user_id, message):
        self.user_id = user_id
        self.message = message

    def __repr__(self):
        return f"<Chat(user_id='{self.user_id}', message='{self.message}')>"