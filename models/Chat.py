#!/usr/bin/python3
from datetime import datetime
from db import db
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from models.BaseModel import BaseModel  # Inheriting from BaseModel

class Chat(BaseModel):
    __tablename__ = 'chats'

    sender_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    receiver_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    message = db.Column(db.String(255), nullable=False)

    sender = db.relationship('User', foreign_keys=[sender_id], backref='sent_chats')
    receiver = db.relationship('User', foreign_keys=[receiver_id], backref='received_chats')

    def __repr__(self):
        return f"<Chat(sender_id='{self.sender_id}', receiver_id='{self.receiver_id}', message='{self.message}')>"
