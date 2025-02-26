#!/usr/bin/python3

BaseModel = __import__('base_model.py').BaseModel

class Amentity(BaseModel):
    def __init__(self, name):
        super().__init__()
        self.name = name
