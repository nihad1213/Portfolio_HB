#!/usr/bin/python3
from sqlalchemy import Column, Integer, String, Boolean
from models.BaseModel import BaseModel, db
from werkzeug.security import generate_password_hash, check_password_hash

class User(BaseModel):
    __tablename__ = 'users'

    name = Column(String(100), nullable=False)
    surname = Column(String(100), nullable=False)
    username = Column(String(100), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    email = Column(String(150), nullable=False, unique=True)
    attend = Column(Boolean, default=False)
    profile_image = Column(String(255), nullable=True)
    description = Column(String(500), nullable=True)
    phone_number = Column(String(20), nullable=True) 
    is_subscribed = Column(Boolean, default=False) 

    def __init__(self, name, surname, username, password, email, attend=False, profile_image=None, description=None, phone_number=None):
        self.name = name
        self.surname = surname
        self.username = username 
        self.password = generate_password_hash(password)
        self.email = email
        self.attend = attend
        self.profile_image = profile_image 
        self.description = description 
        self.phone_number = phone_number 

    @classmethod
    def find_by_email(cls, email):
        return db.session.query(cls).filter_by(email=email).first()

    @classmethod
    def find_by_username(cls, username):
        return db.session.query(cls).filter_by(username=username).first()

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def set_password(self, new_password):
        """Set a new password for the user."""
        self.password = generate_password_hash(new_password)
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return (f"<User(username='{self.username}', name='{self.name}', surname='{self.surname}', "
                f"email='{self.email}', attend={self.attend}, profile_image='{self.profile_image}', "
                f"description='{self.description}', phone_number='{self.phone_number}', "
                f"is_subscribed={self.is_subscribed})>")
