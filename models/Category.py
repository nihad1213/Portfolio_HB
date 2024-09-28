#!/usr/bin/python3
from sqlalchemy import Column, String, DateTime
from models.BaseModel import BaseModel

class Category(BaseModel):
    __tablename__ = 'categories'

    name = Column(String(100), nullable=False)
    category_image = Column(String(255), nullable=True)

    def __init__(self, name, category_image=None):
        self.name = name
        self.category_image = category_image

    def __repr__(self):
        return f"<Category(name='{self.name}', category_image='{self.category_image}')>"
