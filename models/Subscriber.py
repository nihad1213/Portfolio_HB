#!/usr/bin/python3
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from models.BaseModel import BaseModel

class Subscribers(BaseModel):
    __tablename__ = 'subscribers'
    
    email = Column(String(120), nullable=False, unique=True)

    def __init__(self, email):
        self.email = email

    def __repr__(self):
        return f"<Subscriber {self.email}>"
