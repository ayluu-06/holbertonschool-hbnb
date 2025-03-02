import re
from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.review import Review

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

        # Crear usuario solo si las validaciones pasan
        user = User(**user_data)
        self.user_repo.add(user)
        return user
    def get_user_by_email(self, email):
        return User.query.filter_by(email=email).first()
    
# 🏨 Amenities
    
    def create_amenity(self, amenity_data):
        amenity = Amenity(**amenity_data)
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
        if amenity:
            for key, value in amenity_data.items():
                setattr(amenity, key, value)
        return amenity

# 🏠 Places
    
    def create_place(self, place_data):
        # Validar que el propietario existe
        owner = self.user_repo.get_by_id(place_data['owner_id'])
        if not owner:
            raise ValueError("Owner not found.")

        # Validar datos de lugar
        if 'title' not in place_data or 'price' not in place_data or 'latitude' not in place_data or 'longitude' not in place_data:
            raise ValueError("Title, price, latitude, and longitude are required.")

        # Validar que el precio sea un número positivo y razonable
        price = place_data['price']
        if not isinstance(price, (int, float)) or price <= 0:
            raise ValueError("Price must be a positive number.")

        # Validar que la latitud esté en el rango de -90 a 90
        latitude = place_data['latitude']
        if not isinstance(latitude, (int, float)) or latitude < -90 or latitude > 90:
            raise ValueError("Latitude must be between -90 and 90.")

        # Validar que la longitud esté en el rango de -180 a 180
        longitude = place_data['longitude']
        if not isinstance(longitude, (int, float)) or longitude < -180 or longitude > 180:
            raise ValueError("Longitude must be between -180 and 180.")

        # Si pasa lass validaciones crear place
        place = Place(
            title=place_data['title'],
            description=place_data.get('description', ''),
            price=place_data['price'],
            latitude=place_data['latitude'],
            longitude=place_data['longitude'],
            owner=place_data['owner_id']
        )
        self.place_repo.add(place)
        return place

    def get_place(self, place_id):
        place = self.place_repo.get_by_id(place_id)
        if not place:
            raise ValueError("Place not found.")

        owner = self.user_repo.get_by_id(place.owner)
        if not owner:
            raise ValueError("Owner not found.")

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

    def get_all_places(self):
        places = self.place_repo.get_all()
        return [{
            'id': place.id,
            'title': place.title,
            'latitude': place.latitude,
            'longitude': place.longitude
        } for place in places]

    def update_place(self, place_id, place_data):
        place = self.place_repo.get_by_id(place_id)
        if not place:
            raise ValueError("Place not found")

        place.title = place_data.get('title', place.title)
        place.description = place_data.get('description', place.description)
        place.price = place_data.get('price', place.price)
        place.latitude = place_data.get('latitude', place.latitude)
        place.longitude = place_data.get('longitude', place.longitude)

        self.place_repo.update(place)
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
