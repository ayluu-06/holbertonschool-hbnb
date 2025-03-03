import uuid
from app.models.base_model import BaseModel
from app.models.amenity import Amenity

class Place(BaseModel):
    def __init__(self, title, description, price, latitude, longitude, owner_id):
        super().__init__()

        # Validaciones de entrada
        self.id = str(uuid.uuid4())
        self.title = self._validate_title(title)
        self.description = self._validate_description(description)
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner_id = self._validate_owner(owner_id)

        self.reviews = []
        self.amenities = []

    # Funciones de validación
    def _validate_title(self, title):
        if not title:
            raise ValueError("Title cannot be empty")
        return title

    def _validate_description(self, description):
        if not description:
            raise ValueError("Description cannot be empty")
        return description

    def _validate_owner(self, owner):
        if not owner:
            raise ValueError("Owner cannot be empty")
        # Validar que el owner sea un UUID
        try:
            # Si el `owner` es un string, intentar convertirlo a un UUID
            if isinstance(owner, str):
                owner = uuid.UUID(owner)
            elif not isinstance(owner, uuid.UUID):
                raise ValueError("Owner must be a valid UUID.")
        except ValueError:
            raise ValueError("Owner must be a valid UUID.")

        return owner

    # Funciones para agregar reseñas y amenidades
    def add_review(self, review):
        self.reviews.append(review)

    # Función para agregar una amenidad
    def add_amenity(self, amenity):
        if not isinstance(amenity, Amenity):
            raise ValueError("Only Amenity instances can be added.")
        if amenity not in self.amenities:
            self.amenities.append(amenity)

    # Propiedad para price
    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        if not isinstance(value, (int, float)) or value < 0:
            raise ValueError("Price must be a non-negative float.")
        self._price = float(value)

    @property
    def latitude(self):
        return self._latitude

    @latitude.setter
    def latitude(self, value):
        if not isinstance(value, (int, float)) or not (-90 <= value <= 90):
            raise ValueError("Latitude must be between -90 and 90.")
        self._latitude = float(value)

    @property
    def longitude(self):
        return self._longitude

    @longitude.setter
    def longitude(self, value):
        if not isinstance(value, (int, float)) or not (-180 <= value <= 180):
            raise ValueError("Longitude must be between -180 and 180.")
        self._longitude = float(value)

    def to_dict(self):
        return {
            "title": self.title,
            "description": self.description,
            "price": self.price,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "owner_id": str(self.owner_id)    
               }
    