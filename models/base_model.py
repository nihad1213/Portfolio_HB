import uuid
from datetime from datetime

class BaseModel:
    def __init__(self):
        self.id = str(uuid.uuid4())
        self.created_at = str(datetime.now())
        self.updated_at = str(datetime.now())

    def save(self):
        self.updated_at = str(datetime.now())

    def __str__(self):
        return f"[{self.__class__.__name__}] ({self.id}) {self.__dict__}"