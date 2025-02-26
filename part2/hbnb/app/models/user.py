#!/usr/bin/python3

BaseModel = __import__('base_model.py').BaseModel


class User(BaseModel):
    def __init__(self, first_name, last_name, email, is_admin):
        super().__init__()
        self.first_name = first_name
        self.lastname = last_name
        self.email = email
        self.is_admin = is_admin
        