from models.base_model import BaseModel

class User(BaseModel):
    def __init__(self, email, first_name='', last_name=''):
        super().__init__()
        self.email = email
        self.first_name = first_name
        self.last_name = last_name