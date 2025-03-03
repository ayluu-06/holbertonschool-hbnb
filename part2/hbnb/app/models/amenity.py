from app.models.base_model import BaseModel

class Amenity(BaseModel):
    def __init__(self, name):
        super().__init__()  # Llamar al constructor de BaseModel
        if not name:
            raise ValueError("Name cannot be empty")
        self.name = name

    def to_dict(self):
        # Convierte el objeto en un diccionario
        return {
            'id': self.id,
            'name': self.name,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }