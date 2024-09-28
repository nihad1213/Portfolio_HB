#!/usr/bin/python3

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import uuid

# Initialize the SQLAlchemy object
from db import db

class BaseModel(db.Model):
    __abstract__ = True  # Doesnt create table in database

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def save(self):
        self.updated_at = datetime.utcnow()
        db.session.add(self)
        db.session.commit()

    def __str__(self):
        return f"[{self.__class__.__name__}] ({self.id}) {self.__dict__}"
