from app.persistence.repository import InMemoryRepository
from app.models.place import Place

class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()
    
    def create_place(self, place_data):
        place = Place(
            title=place_data['title'],
            description=place_data.get('description', ''),
            price=place_data['price'],
            latitude=place_data['latitude'],
            longitude=place_data['longitude'],
            owner=place_data['owner_id']
        )
        self.place_repo.save(place)
        return place

    def get_place(self, place_id):
        place = self.place_repo.get_by_id(place_id)
        if place:
            owner = self.user_repo.get_by_id(place.owner)
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