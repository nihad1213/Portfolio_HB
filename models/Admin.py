#!/usr/bin/python3

from sqlalchemy import Column, String
from werkzeug.security import generate_password_hash, check_password_hash
from models.BaseModel import BaseModel
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Admin(BaseModel):
    __tablename__ = 'admins'

    username = Column(String(100), nullable=False, unique=True)
    email = Column(String(100), nullable=False, unique=True)
    password_hash = Column(String(255), nullable=False)

    def __init__(self, username=None, email=None, password=None, *args, **kwargs):
        """Initialize the Admin object and set password if provided."""
        super().__init__(*args, **kwargs)
        self.username = username
        self.email = email
        if password:
            self.set_password(password)

    def set_password(self, password):
        """Hash the password and store it."""
        try:
            self.password_hash = generate_password_hash(password)
            logger.info(f"Password for {self.username} hashed successfully.")
        except Exception as e:
            logger.error(f"Error hashing password for {self.username}: {str(e)}")
            raise

    def check_password(self, password):
        """Check if the provided password matches the stored hash."""
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<Admin(username='{self.username}', email='{self.email}')>"
