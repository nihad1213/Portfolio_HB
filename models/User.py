#!/usr/bin/python3
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from models.BaseModel import BaseModel, db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class User(BaseModel):
    __tablename__ = 'users'

    name = Column(String(100), nullable=False)
    surname = Column(String(100), nullable=False)
    username = Column(String(100), nullable=False, unique=True)  # New username field
    password = Column(String(255), nullable=False)
    email = Column(String(150), nullable=False, unique=True)
    attend = Column(Boolean, default=False)

    def __init__(self, name, surname, username, password, email, attend=False):
        self.name = name
        self.surname = surname
        self.username = username  # Initialize username
        self.password = generate_password_hash(password)
        self.email = email
        self.attend = attend

    @classmethod
    def find_by_email(cls, email):
        return db.session.query(cls).filter_by(email=email).first()

    @classmethod
    def find_by_username(cls, username):
        return db.session.query(cls).filter_by(username=username).first()

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return f"<User(username='{self.username}', name='{self.name}', surname='{self.surname}', email='{self.email}', attend={self.attend})>"