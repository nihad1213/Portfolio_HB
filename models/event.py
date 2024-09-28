#!/usr/bin/python3

class Event(BaseModel):
    table = 'events'

    def __init__(self, title, date, location, category, image, description, registration):
        super().__init__()
        self.title = title
        self.date = date
        self.location = location
        self.category = category
        self.image = image
        self.description = description
        self.registration = registration

    def save(self):
        super().save()

    def __str__(self):
        return f"{super().__str__()} | Title: {self.title}, Date: {self.date}, Location: {self.location}, Category: {self.category.name}, Image: {self.image}, Description: {self.description}, Registration: {self.registration}"
