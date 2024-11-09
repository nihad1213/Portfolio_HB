from sqlalchemy import Column, ForeignKey, String
from models.BaseModel import BaseModel
from db import db

class Like(BaseModel):
    __tablename__ = 'likes'
    
    user_id = Column(String(36), ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    event_id = Column(String(36), ForeignKey('events.id', ondelete='CASCADE'), nullable=False)
    
    def __init__(self, user_id, event_id):
        super().__init__()  # Call parent's __init__
        self.user_id = str(user_id)  # Ensure string type
        self.event_id = str(event_id)  # Ensure string type