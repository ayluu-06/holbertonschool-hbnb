import pytest
from app.models.place import Place
from app.models.amenity import Amenity

@pytest.fixture
def setup_place_and_amenity():
    # Configura un lugar y una amenidad para usar en los tests
    place = Place(title="Cozy Apartment", description="A nice place to stay", price=100, latitude=37.7749, longitude=-122.4194, owner="John Doe")
    amenity = Amenity(name="Pool")
    return place, amenity

def test_add_valid_amenity(setup_place_and_amenity):
    place, amenity = setup_place_and_amenity
    # Agregar la amenidad
    place.add_amenity(amenity)
    
    # Verificar que la amenidad se haya añadido correctamente
    assert amenity in place.amenities

def test_add_duplicate_amenity(setup_place_and_amenity):
    place, amenity = setup_place_and_amenity
    # Agregar la amenidad dos veces
    place.add_amenity(amenity)
    place.add_amenity(amenity)  # Intentar agregarla de nuevo
    
    # Verificar que no se haya duplicado
    assert place.amenities.count(amenity) == 1

def test_add_multiple_amenities(setup_place_and_amenity):
    place, amenity = setup_place_and_amenity
    amenity2 = Amenity(name="Gym")
    
    # Agregar varias amenidades
    place.add_amenity(amenity)
    place.add_amenity(amenity2)
    
    # Verificar que ambas amenidades están presentes
    assert amenity in place.amenities
    assert amenity2 in place.amenities
