import uuid
from app import db
from app.models.base_model import BaseModel

# Tabla de relación entre lugares y amenidades
# Relationship table between places and amenities


class Amenity(BaseModel):
    __tablename__ = 'amenities'  # Nombre de la tabla en la base de datos / Table name in the database

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
  # ID único de la amenidad / Unique amenity ID
    name = db.Column(db.String(100), nullable=False)  # Nombre de la amenidad (obligatorio) / Amenity name (required)
    description = db.Column(db.Text, nullable=True)  # Descripción opcional / Optional description

    def __init__(self, name, description=None):
        """
        Constructor de la clase Amenity
        Amenity class constructor
        """
        super().__init__()
        if not name:
            raise ValueError("Name cannot be empty")  # Validación: el nombre no puede estar vacío / Validation: name cannot be empty
        self.name = name
        self.description = description

    def to_dict(self):
        """
        Convierte el objeto en un diccionario para ser retornado en la API
        
        Converts the object into a dictionary to be returned in the API
        """
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
