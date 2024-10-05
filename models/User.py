#!/usr/bin/python3
from sqlalchemy import Column, Integer, String, Boolean
from models.BaseModel import BaseModel, db  # Ensure db is correctly imported for sessions
from werkzeug.security import generate_password_hash, check_password_hash

class User(BaseModel, db.Model):  # Inherit from db.Model to use SQLAlchemy ORM
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    surname = Column(String(100), nullable=False)
    password = Column(String(255), nullable=False)
    email = Column(String(150), nullable=False, unique=True)
    attend = Column(Boolean, default=False)

    def __init__(self, name, surname, password, email, attend=False):
        self.name = name
        self.surname = surname
        self.password = generate_password_hash(password)  # Securely hash the password
        self.email = email
        self.attend = attend

    @classmethod
    def find_by_email(cls, email):
        """Query a user by their email."""
        return cls.query.filter_by(email=email).first()

    def check_password(self, password):
        """Check if the provided password matches the hashed password."""
        return check_password_hash(self.password, password)

    def save(self):
        """Insert or update the user in the database."""
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return f"<User(name='{self.name}', surname='{self.surname}', email='{self.email}', attend={self.attend})>"
