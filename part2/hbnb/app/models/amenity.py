#!/usr/bin/python3
from app.models.base_model import BaseModel

class Amenity(BaseModel):
    def __init__(self, name):
        super().__init__()
        if not name:
            raise ValueError("Name cannot be empty")
        self.name = name

    def to_dict(self):
        # retorna un diccionario con los atributos del objeto
        return {
            'id': self.id,
            'name': self.name,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
