#!/usr/bin/python3

# Importing Modules
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from models.BaseModel import BaseModel, db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class User(BaseModel):
    __tablename__ = 'users'

    name = Column(String(100), nullable=False)
    surname = Column(String(100), nullable=False)
    username = Column(String(100), nullable=False, unique=True)
    email = Column(String(150), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    birth_date = Column(DateTime, nullable=False)
    attend = Column(Boolean, default=False)

    def __init__(self, name, surname, username, email, password, birth_date, attend=False):
        self.name = name
        self.surname = surname
        self.username = username
        self.email = email
        self.password = generate_password_hash(password)
        self.birth_date = birth_date
        self.attend = attend

    @classmethod
    def find_by_email(cls, email):
        """Query a user by their email."""
        return db.session.query(cls).filter_by(email=email).first()

    def check_password(self, password):
        """Check if the provided password matches the hashed password."""
        return check_password_hash(self.password, password)

    def save(self):
        """Insert or update the user in the database."""
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

    def __repr__(self):
        return f"<User(name='{self.name}', surname='{self.surname}', email='{self.email}', attend={self.attend})>"
