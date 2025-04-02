import uuid
from app import db
from app.models.base_model import BaseModel
from app.models.amenity import Amenity

# Definición de la tabla de relación entre Place y Amenity
# Relationship table between Place and Amenity
place_amenity = db.Table(
    'place_amenity',
    db.metadata,
    db.Column('place_id', db.Integer, db.ForeignKey('places.id'), primary_key=True),
    db.Column('amenity_id', db.Integer, db.ForeignKey('amenities.id'), primary_key=True),
    extend_existing=True
)

class Place(BaseModel):
    __tablename__ = 'places'

    # Definición de las columnas de la base de datos
    # Database column definitions
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    owner_id = db.Column(db.String(36), nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Relaciones con otras tablas
    # Relationships with other tables
    reviews = db.relationship('Review', backref='place', lazy=True)
    amenities = db.relationship('Amenity', secondary=place_amenity, backref='places', lazy=True)

    def __init__(self, title, description, price, latitude, longitude, owner_id):
        super().__init__()

        # Validaciones de entrada
        # Input validations
        self.title = self._validate_title(title)
        self.description = self._validate_description(description)
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner_id = self._validate_owner(owner_id)

    # Funciones de validación
    # Validation functions
    def _validate_title(self, title):
        if not title:
            raise ValueError("Title cannot be empty / El título no puede estar vacío")
        return title

    def _validate_description(self, description):
        if not description:
            raise ValueError("Description cannot be empty / La descripción no puede estar vacía")
        return description

    def _validate_owner(self, owner):
        if not owner:
            raise ValueError("Owner cannot be empty / El propietario no puede estar vacío")
        try:
            if isinstance(owner, str):
                owner = uuid.UUID(owner)
            elif not isinstance(owner, uuid.UUID):
                raise ValueError("Owner must be a valid UUID / El propietario debe ser un UUID válido")
        except ValueError:
            raise ValueError("Owner must be a valid UUID / El propietario debe ser un UUID válido")
        return owner

    # Funciones para agregar reseñas y amenidades
    # Functions to add reviews and amenities
    def add_review(self, review):
        self.reviews.append(review)

    def add_amenity(self, amenity):
        if not isinstance(amenity, Amenity):
            raise ValueError("Only Amenity instances can be added / Solo se pueden agregar instancias de Amenity")
        if amenity not in self.amenities:
            self.amenities.append(amenity)

    # Propiedades con validaciones
    # Properties with validations
    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        if not isinstance(value, (int, float)) or value < 0:
            raise ValueError("Price must be a non-negative float / El precio debe ser un número positivo")
        self._price = float(value)

    @property
    def latitude(self):
        return self._latitude

    @latitude.setter
    def latitude(self, value):
        if not isinstance(value, (int, float)) or not (-90 <= value <= 90):
            raise ValueError("Latitude must be between -90 and 90 / La latitud debe estar entre -90 y 90")
        self._latitude = float(value)

    @property
    def longitude(self):
        return self._longitude

    @longitude.setter
    def longitude(self, value):
        if not isinstance(value, (int, float)) or not (-180 <= value <= 180):
            raise ValueError("Longitude must be between -180 and 180 / La longitud debe estar entre -180 y 180")
        self._longitude = float(value)

    # Método para convertir el objeto a diccionario
    # Method to convert the object to a dictionary
    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "price": self.price,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "owner_id": str(self.owner_id),
            "reviews": [review.to_dict() for review in self.reviews],
            "amenities": [amenity.to_dict() for amenity in self.amenities]
        }
