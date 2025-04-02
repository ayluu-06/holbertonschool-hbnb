import uuid
from app import db
from app.models.base_model import BaseModel

class Review(BaseModel):
    __tablename__ = 'reviews'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    text = db.Column(db.String(1024), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    place_id = db.Column(db.String(36), db.ForeignKey('places.id'), nullable=False)

    def __init__(self, text, rating, place_id, user_id):
        """Inicializa una nueva instancia de Review"""
        super().__init__()
        self.text = text
        self.rating = rating
        self.place_id = place_id
        self.user_id = user_id

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("El texto de la reseña no puede estar vacío.")
        self._text = value

    @property
    def rating(self):
        return self._rating

    @rating.setter
    def rating(self, value):
        if not isinstance(value, int) or not (1 <= value <= 5):
            raise ValueError("La calificación debe estar entre 1 y 5.")
        self._rating = value

    def to_dict(self):
        """Convierte la reseña a un diccionario para la API"""
        return {
            "id": self.id,
            "text": self.text,
            "rating": self.rating,
            "user_id": self.user_id,
            "place_id": self.place_id,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }
