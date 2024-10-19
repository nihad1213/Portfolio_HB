#!/usr/bin/python3
from sqlalchemy import Column, String, Boolean
from models.BaseModel import BaseModel, db
from werkzeug.security import generate_password_hash, check_password_hash

class User(BaseModel, db.Model):  # Inherit from db.Model to use SQLAlchemy ORM
    __tablename__ = 'users'

    id = db.Column(db.String(36), primary_key=True)  # Ensure this is correct
    name = db.Column(String(100), nullable=False)
    surname = db.Column(String(100), nullable=False)
    username = db.Column(String(100), nullable=False, unique=True)
    password = db.Column(String(255), nullable=False)
    email = db.Column(String(150), nullable=False, unique=True)
    attend = db.Column(Boolean, default=False)
    profile_image = db.Column(String(255), nullable=True)
    description = db.Column(String(500), nullable=True)
    phone_number = db.Column(String(20), nullable=True)
    is_subscribed = db.Column(Boolean, default=False)

    def __init__(self, name, surname, username, password, email, attend=False, profile_image=None, description=None, phone_number=None):
        self.name = name
        self.surname = surname
        self.username = username
        self.password = generate_password_hash(password)  # Store hashed password
        self.email = email
        self.attend = attend
        self.profile_image = profile_image
        self.description = description
        self.phone_number = phone_number

    @classmethod
    def find_by_email(cls, email):
        """Find user by email."""
        return db.session.query(cls).filter_by(email=email).first()

    @classmethod
    def find_by_username(cls, username):
        """Find user by username."""
        return db.session.query(cls).filter_by(username=username).first()

    def check_password(self, password):
        """Check if the provided password matches the stored hash."""
        return check_password_hash(self.password, password)

    def set_password(self, new_password):
        """Set a new password for the user."""
        self.password = generate_password_hash(new_password)

    def save(self):
        """Save the user to the database."""
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return (f"<User(username='{self.username}', name='{self.name}', surname='{self.surname}', "
                f"email='{self.email}', attend={self.attend}, profile_image='{self.profile_image}', "
                f"description='{self.description}', phone_number='{self.phone_number}', "
                f"is_subscribed={self.is_subscribed})>")
