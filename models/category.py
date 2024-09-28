#!/usr/bin/python3

class Category(BaseModel):
    table = 'categories'

    def __init__(self, name, category_image):
        super().__init__()
        self.name = name
        self.category_image = category_image

    def save(self):
        """Insert or update the category in the database."""
        super().save()

    def __str__(self):
        return f"{super().__str__()} | Name: {self.name}, Image: {self.category_image}"
