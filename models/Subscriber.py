#!/usr/bin/python3
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from models.BaseModel import BaseModel

class Subscriber(BaseModel):
    __tablename__ = 'subscribers'

    user_id = Column(String(36), ForeignKey('users.id'), nullable=False)  # Foreign key to User

    def __init__(self, user_id):
        self.user_id = user_id

    def __repr__(self):
        return f"<Subscriber(user_id='{self.user_id}')>"
