from app.models.base_model import BaseModel
from app.models.place import Place
from app.models.user import User

class Review(BaseModel):
    def __init__(self, text, rating, place, user):
        super().__init__()

        # Validaciones de entrada
        self.text = self._validate_text(text)  # Usa el setter para text
        self.rating = self._validate_rating(rating)
        self.place = self._validate_place(place)
        self.user = self._validate_user(user)

    # Función que valida que text tenga más de 10 caracteres
    def _validate_text(self, text):
        if not text:
            raise ValueError("Text cannot be empty")
        if len(text) < 10:
            raise ValueError("Text must be at least 10 characters long")
        return text

    # Función que valida que rating esté entre 1 y 5
    def _validate_rating(self, rating):
        if not isinstance(rating, (int, float)):
            raise ValueError("Rating must be a number")
        if not (1 <= rating <= 5):
            raise ValueError("Rating must be between 1 and 5")
        return rating
    
    # Función que valida que place sea una instancia de Place
    def _validate_place(self, place):
        if not isinstance(place, Place):
            raise ValueError("Place must be an instance of the Place class")
        return place

    # Función que valida que user sea una instancia de User
    def _validate_user(self, user):
        if not isinstance(user, User):
            raise ValueError("User must be an instance of the User class")
        return user

    # Propiedad para text
    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        self._text = self._validate_text(value)

    # Propiedad para rating
    @property
    def rating(self):
        return self._rating

    @rating.setter
    def rating(self, value):
        self._rating = self._validate_rating(value)

    # Propiedad para place
    @property
    def place(self):
        return self._place

    @place.setter
    def place(self, value):
        self._place = self._validate_place(value)

    # Propiedad para user
    @property
    def user(self):
        return self._user

    @user.setter
    def user(self, value):
        self._user = self._validate_user(value)
