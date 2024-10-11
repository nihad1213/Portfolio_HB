#!/usr/bin/python3

from sqlalchemy import Column, String
from werkzeug.security import generate_password_hash, check_password_hash
from models.BaseModel import BaseModel

class Admin(BaseModel):
    __tablename__ = 'admins'

    username = Column(String(100), nullable=False, unique=True)
    email = Column(String(100), nullable=False, unique=True)
    password_hash = Column(String(255), nullable=False)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.set_password(password)

    def set_password(self, password):
        """Hash the password and store it."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Check if the provided password matches the stored hash."""
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<Admin(username='{self.username}', email='{self.email}')>"
