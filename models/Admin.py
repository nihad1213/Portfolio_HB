#!/usr/bin/python3
from sqlalchemy import Column, String, DateTime
from models.BaseModel import BaseModel
from datetime import datetime

class Admin(BaseModel):
    __tablename__ = 'admins'

    username = Column(String(100), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __repr__(self):
        return f"<Admin(username='{self.username}')>"
