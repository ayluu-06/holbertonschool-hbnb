import re
from app.persistence.repository import UserRepository
from app.persistence.repository import SQLAlchemyRepository
from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.review import Review
from datetime import datetime

class HBnBFacade:
    def __init__(self, db_instance):
       self.db = db_instance
       self.user_repo = UserRepository(db_instance)
       self.amenity_repo = SQLAlchemyRepository(Amenity, db_instance)
       self.place_repo = SQLAlchemyRepository(Place, db_instance)
       self.review_repo = SQLAlchemyRepository(Review, db_instance)

    

# 👨 users
class UserService:
    
    def __init__(self, user_repo):
        self.user_repo = user_repo  # Aquí inyectamos el repositorio de usuarios

    def create_user(self, user_data):
        # Validar que first_name y last_name no estén vacíos
        if not user_data.get("first_name") or not user_data.get("last_name"):
            raise ValueError("First name and last name are required.")

        # Validar formato del email
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if not re.match(email_regex, user_data.get("email", "")):
            raise ValueError("Invalid email format.")
        
        # Verificar si el correo ya está registrado
        existing_user = self.get_user_by_email(user_data.get("email"))
        if existing_user:
            raise ValueError("Email already registered")

        # Crear usuario solo si las validaciones pasan
        new_user = User(
            first_name=user_data.get("first_name"),
            last_name=user_data.get("last_name"),
            email=user_data.get("email"),
            is_admin=user_data.get("is_admin", False)
        )
        
        # Hashear la contraseña antes de almacenarla
        password = user_data.get("password")
        if not password:
            raise ValueError("Password is required")
        
        new_user.hash_password(password)

        # Almacenar el nuevo usuario en la base de datos
        self.user_repo.add(new_user)

        # Retornar el nuevo usuario creado
        return new_user

    def get_user_by_email(self, email):
        # Buscar un usuario por su correo electrónico
        return self.user_repo.get_by_attribute('email', email)

    def get_all_users(self):
        # Obtener todos los usuarios
        return self.user_repo.get_all()

    def save(self, user):
        # Método para guardar el usuario en la base de datos
        existing_user = self.user_repo.get_by_attribute("email", user.email)
        if existing_user:
            raise ValueError("El usuario ya existe en la base de datos.")
        try:
            self.user_repo.add(user)
            self.user_repo.commit()
        except Exception as e:
            self.user_repo.rollback()
            raise ValueError(f"Error guardando el usuario: {str(e)}")
    
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
    # Obtener la amenidad antes de eliminarla
        amenity = self.get_amenity(amenity_id)
        if not amenity:
            raise ValueError("Amenity not found.")

        try:
            # Eliminar la amenidad
            self.db.session.delete(amenity)
            self.db.session.commit()
            return {"message": "Amenity deleted successfully"}
        except Exception as e:
            self.db.session.rollback()
            raise ValueError(f"Error deleting amenity: {str(e)}")


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
        amenities = [self.amenity_repo.get(amenity_id) for amenity_id in place_data['amenities'] if self.amenity_repo.get(amenity_id)]

        # Si algún ID no se encontró, lanzar un error
        missing_ids = [amenity_id for amenity_id in place_data['amenities'] if not self.amenity_repo.get(amenity_id)]
        if missing_ids:
            raise ValueError(f"Amenities not found for IDs: {missing_ids}")

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
        place.amenities.extend(amenities)  


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
            owner = self.user_repo.get(place.owner_id)
            amenities = self.amenity_repo.get_by_place_id(place_id)
            return {
                'id': place.id,
                'title': place.title,
                'description': place.description,
                'price': place.price,
                'latitude': place.latitude,
                'longitude': place.longitude,
                'owner': {
                    'id': owner.id,
                    'first_name': owner.first_name,
                    'last_name': owner.last_name,
                    'email': owner.email
                },
                'amenities': [{'id': amenity.id, 'name': amenity.name} for amenity in amenities]
            }
        return None

    
    def get_all_places(self):
        places = self.place_repo.get_all()
        return [{
            'id': place.id,
            'title': place.title,
            'latitude': place.latitude,
            'longitude': place.longitude
        } for place in places]

    def update_place(self, place_id, place_data):
        place = self.place_repo.get(place_id)
        if not place:
            raise ValueError("Place not found")

        place.title = place_data.get('title', place.title)
        place.description = place_data.get('description', place.description)
        place.price = place_data.get('price', place.price)
        place.latitude = place_data.get('latitude', place.latitude)
        place.longitude = place_data.get('longitude', place.longitude)

        self.place_repo.update(place)
        self.db.session.commit()
        return place
    
# 📝 Review

    def create_review(self, review_data):
        try:
            # Verificar que los datos de review sean correctos
            if 'text' not in review_data or not review_data['text']:
                raise ValueError("Review text is required.")
            if 'rating' not in review_data or not isinstance(review_data['rating'], (int, float)):
                raise ValueError("Valid rating is required.")

            user = self.user_repo.get(review_data['user_id'])
            place = self.place_repo.get(review_data['place_id'])

            # Validar si los objetos existen
            if not user or not place:
                raise ValueError("Invalid user_id or place_id.")

            # Crear la review
            review = Review(
                text=review_data['text'],
                rating=review_data['rating'],
                user_id=user.id,
                place_id=place.id
            )

            self.review_repo.add(review)
            return review.to_dict()
    
        except Exception as e:
            print(f"Error al crear la review: {e}")
            return {"error": str(e)}



    def get_review(self, review_id):
        review = self.review_repo.get(review_id)
        if not review:
            raise ValueError("Review not found.")
        return review

    def get_all_reviews(self):
        reviews = self.review_repo.get_all()
        return [review.to_dict() for review in reviews]
     

    def get_reviews_by_place(self, place_id):
        try:
            reviews = self.review_repo.get_reviews_by_place(place_id)
            return [review.to_dict() for review in reviews] if reviews else []
        except Exception as e:
            print(f"Error fetching reviews: {e}")
            return []

    def update_review(self, review_id, review_data):
        review = self.get_review(review_id)
        if not review:
            raise ValueError("Review not found.")
        if 'text' in review_data:
            review.text = review_data['text']
        if 'rating' in review_data:
            review.rating = review_data['rating']

        self.review_repo.update(review)
        self.db.session.commit()
        return review

    def delete_review(self, review_id):
        review = self.get_review(review_id)
        if not review:
            raise ValueError("Review not found.")
        self.review_repo.delete(review_id)
        self.db.session.commit()
        return {"message": "Review deleted successfully"}