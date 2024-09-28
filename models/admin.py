#!/usr/bin/python3

class Admin(BaseModel):
    table = 'admins'

    def __init__(self, username, password):
        super().__init__()
        self.username = username
        self.password = password

    def save(self):
        """Insert or update the admin in the database."""
        super().save()

    def __str__(self):
        return f"{super().__str__()} | Username: {self.username}"
