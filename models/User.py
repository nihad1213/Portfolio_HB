#!/usr/bin/python3
from sqlalchemy import Column, Integer, String, Boolean
from models.BaseModel import BaseModel, db
from datetime import datetime

class User(BaseModel):
    __tablename__ = 'users'

    name = Column(String(100), nullable=False)
    surname = Column(String(100), nullable=False)
    password = Column(String(255), nullable=False)
    email = Column(String(150), nullable=False, unique=True)
    attend = Column(Boolean, default=False)

    def __init__(self, name, surname, password, email, attend=False):
        self.name = name
        self.surname = surname
        self.password = password
        self.email = email
        self.attend = attend

    def save(self, session):
        """Insert or update the user in the database."""
        session.add(self)
        session.commit()

    def __repr__(self):
        return f"<User(name='{self.name}', surname='{self.surname}', email='{self.email}', attend={self.attend})>"
