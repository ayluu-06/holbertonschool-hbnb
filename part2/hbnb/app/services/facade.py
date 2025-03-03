import re
from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.review import Review
from datetime import datetime
from flask import jsonify

class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()

# 👨 users
    def create_user(self, user_data):
        # Validar que first_name y last_name no estén vacíos
        if not user_data.get("first_name") or not user_data.get("last_name"):
            raise ValueError("First name and last name are required.")

        # Validar formato del email
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if not re.match(email_regex, user_data.get("email", "")):
            raise ValueError("Invalid email format.")
        
        existing_user = self.get_user_by_email(user_data.get("email"))
        if existing_user:
            raise ValueError("Email already registered")

        # Crear usuario solo si las validaciones pasan
        user = User(**user_data)
        self.user_repo.add(user)
        return user
    
    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute('email', email)
    
    def get_all_users(self):
        return self.user_repo.get_all()
    
# 🏨 Amenities
    
    def create_amenity(self, amenity_data):
        if "name" not in amenity_data or not amenity_data["name"]:
            raise ValueError("Amenity name is required")

        amenity = Amenity(name=amenity_data["name"])
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        amenity = self.amenity_repo.get(amenity_id)
        if not amenity:
            raise ValueError("Amenity not found.")
        return amenity

    def get_all_amenities(self):
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        amenity = self.get_amenity(amenity_id)

        # Actualizar los campos que han cambiado
        for key, value in amenity_data.items():
            setattr(amenity, key, value)

        # Actualizar la fecha de modificación
        amenity.updated_at = datetime.utcnow()
        return amenity

    def delete_amenity(self, amenity_id):
        amenity = self.get_amenity(amenity_id)
        self.amenity_repo.delete(amenity_id)
        return {"message": "Amenity deleted successfully"}

    def delete_all_amenities(self):
        print("Borrando todos los amenities...")
        self.amenity_repo.delete_all()  
        print("Todos los amenities han sido eliminados.")


# 🏠 Places
    
    def create_place(self, place_data):
        """Crea un nuevo lugar validando los datos proporcionados."""

        # Verificar si 'owner_id' está presente
        if 'owner_id' not in place_data:
            raise ValueError("'owner_id' is required in place_data.")

    # Validar que el propietario existe
        owner = self.user_repo.get(place_data['owner_id'])
        if not owner:
            raise ValueError("Owner not found.")

        # Validar datos de lugar
        required_fields = ['title', 'price', 'latitude', 'longitude']
        for field in required_fields:
            if field not in place_data:
                raise ValueError(f"{field} is required.")

        # Validar precio
        price = place_data['price']
        if not isinstance(price, (int, float)) or price <= 0:
            raise ValueError("Price must be a positive number.")

        # Validar latitud y longitud
        latitude, longitude = place_data['latitude'], place_data['longitude']
        if not (-90 <= latitude <= 90):
            raise ValueError("Latitude must be between -90 and 90.")
        if not (-180 <= longitude <= 180):
            raise ValueError("Longitude must be between -180 and 180.")

        # Validar amenities
        if 'amenities' not in place_data or not isinstance(place_data['amenities'], list) or len(place_data['amenities']) == 0:
            raise ValueError("At least one amenity is required for the place.")

        # Validar que las amenities existan
        amenities = []
        for amenity_id in place_data['amenities']:
            amenity = self.amenity_repo.get(amenity_id)
            if amenity:
                amenities.append(amenity)
            else:
                raise ValueError(f"Amenity with ID {amenity_id} not found.")

        # Crear el lugar
        place = Place(
            title=place_data['title'],
            description=place_data.get('description', ''),
            price=place_data['price'],
            latitude=place_data['latitude'],
            longitude=place_data['longitude'],
            owner_id=place_data['owner_id']
                      )

        # **Importante**: Asegurar que place.amenities es una lista antes de agregar elementos
        place.amenities = []  

        # Asignar amenities correctamente
        for amenity in amenities:
            place.add_amenity(amenity)

        # Guardar el lugar en la base de datos/repositorio
        self.place_repo.add(place)

        # **Asegurar que place tiene ID antes de retornarlo**
        return {
            "id": str(place.id),
            "title": place.title,
            "description": place.description,
            "price": place.price,
            "latitude": place.latitude,
            "longitude": place.longitude,
            "owner_id": str(place.owner_id),
            "amenities": [str(amenity.id) for amenity in place.amenities]
                         }, 201
    
    def get_place(self, place_id):
        """Recupera un lugar por su ID desde el repositorio."""

        # Buscar el lugar directamente usando el ID
        place = self.place_repo.get(place_id)
        if place:
            return place
        return None
    
    def get_all_places(self):
        """Recupera todos los lugares desde el repositorio."""
        places = self.place_repo.get_all()
        if places:
            return places
        return [] 
    
    def update_place(self, place_id, updated_data):
        """Actualiza los detalles de un lugar existente."""
        # Buscar el lugar en el repositorio por su ID
        place = self.place_repo.get(place_id)
    
        if not place:
            raise ValueError("Place not found")  # Si el lugar no se encuentra, lanza un error
    
        # Actualizar los campos del lugar con los nuevos datos
        for key, value in updated_data.items():
            if hasattr(place, key):
                setattr(place, key, value)
    
    
        self.update_at = datetime.utcnow()
        return place 
    
# 📝 Review

    def create_review(self, review_data):
        user = self.user_repo.get_by_id(review_data['user_id'])
        place = self.place_repo.get_by_id(review_data['place_id'])
        if not user or not place:
            raise ValueError("Invalid user_id or place_id.")

        review = Review(
            text=review_data['text'],
            rating=review_data['rating'],
            user_id=review_data['user_id'],
            place_id=review_data['place_id']
        )
        self.review_repo.add(review)
        return review

    def get_review(self, review_id):
        review = self.review_repo.get(review_id)
        if not review:
            raise ValueError("Review not found.")
        return review

    def get_all_reviews(self):
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        return self.review_repo.get_by_attribute('place_id', place_id)

    def update_review(self, review_id, review_data):
        review = self.get_review(review_id)
        if not review:
            raise ValueError("Review not found.")

        if 'text' in review_data:
            review.text = review_data['text']
        if 'rating' in review_data:
            review.rating = review_data['rating']

        self.review_repo.update(review)
        return review

    def delete_review(self, review_id):
        review = self.get_review(review_id)
        if not review:
            raise ValueError("Review not found.")
        self.review_repo.delete(review_id)
