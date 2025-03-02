#!/usr/bin/python3

from app.models.base_model import BaseModel
from app.models.amenity import Amenity

class Place(BaseModel):
    def __init__(self, title, description, price, latitude, longitude, owner):
        super().__init__()

        # Validaciones de entrada
        self.title = self._validate_title(title)
        self.description = self._validate_description(description)
        self.price = price 
        self.latitude = latitude
        self.longitude = longitude
        self.owner = self._validate_owner(owner)

        # Inicialización de reseñas y servicios
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
        return owner

    # funciones para agregar reseñas y amenidades
    def add_review(self, review):
        self.reviews.append(review)
    
    # funcion para agregar una amenidad
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

    # Propiedad para latitude
    @property
    def latitude(self):
        return self._latitude

    @latitude.setter
    def latitude(self, value):
        if not isinstance(value, (int, float)) or not (-90 <= value <= 90):
            raise ValueError("Latitude must be between -90 and 90.")
        self._latitude = float(value)

    # Propiedad para longitude
    @property
    def longitude(self):
        return self._longitude

    @longitude.setter
    def longitude(self, value):
        if not isinstance(value, (int, float)) or not (-180 <= value <= 180):
            raise ValueError("Longitude must be between -180 and 180.")
        self._longitude = float(value)
