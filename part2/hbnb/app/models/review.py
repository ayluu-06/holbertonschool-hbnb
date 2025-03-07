from app.models.base_model import BaseModel
from app.models.place import Place
from app.models.user import User

class Review(BaseModel):
    def __init__(self, text, rating, place, user):
        super().__init__()

        # Validar que 'place' y 'user' sean instancias correctas
        self.place = self._validate_place(place)
        self.user = self._validate_user(user)

        # Validaciones de entrada
        self.text = self._validate_text(text)
        self.rating = self._validate_rating(rating)

    # Validación de texto
    def _validate_text(self, text):
        if not text:
            raise ValueError("Text cannot be empty")
        if len(text) < 10:
            raise ValueError("Text must be at least 10 characters long")
        return text

    # Validación de rating
    def _validate_rating(self, rating):
        if not isinstance(rating, (int, float)):
            raise ValueError("Rating must be a number")
        if not (1 <= rating <= 5):
            raise ValueError("Rating must be between 1 and 5")
        return rating

    # Validación de place
    def _validate_place(self, place):
        if not isinstance(place, Place):
            raise ValueError("Place must be an instance of the Place class")
        return place

    # Validación de user
    def _validate_user(self, user):
        if not isinstance(user, User):
            raise ValueError("User must be an instance of the User class")
        return user

    # Método para convertir el objeto a un diccionario
    def to_dict(self):
        
        print(f"created_at: {self.created_at} ({type(self.created_at)})")
        print(f"updated_at: {self.updated_at} ({type(self.updated_at)})")

        return {
            "id": str(self.id),
            "text": self.text,
            "rating": self.rating,
            "place_id": str(self.place.id),
            "user_id": str(self.user.id),
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
