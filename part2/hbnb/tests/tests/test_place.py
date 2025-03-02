import pytest
from app.models.place import Place

# Prueba de creación de un Place válido
def test_create_place_valid():
    place = Place(title="Beach House", description="A lovely beach house.", price=150.0, latitude=34.0, longitude=-118.5, owner="John Doe")
    assert place.title == "Beach House"
    assert place.description == "A lovely beach house."
    assert place.price == 150.0
    assert place.latitude == 34.0
    assert place.longitude == -118.5
    assert place.owner == "John Doe"

# Prueba de creación de un Place con título vacío
def test_create_place_empty_title():
    with pytest.raises(ValueError) as exc_info:
        Place(title="", description="A lovely beach house.", price=150.0, latitude=34.0, longitude=-118.5, owner="John Doe")
    assert str(exc_info.value) == "Title cannot be empty"

# Prueba de creación de un Place con descripción vacía
def test_create_place_empty_description():
    with pytest.raises(ValueError) as exc_info:
        Place(title="Beach House", description="", price=150.0, latitude=34.0, longitude=-118.5, owner="John Doe")
    assert str(exc_info.value) == "Description cannot be empty"

# Prueba de creación de un Place con precio negativo
def test_create_place_negative_price():
    with pytest.raises(ValueError) as exc_info:
        Place(title="Beach House", description="A lovely beach house.", price=-150.0, latitude=34.0, longitude=-118.5, owner="John Doe")
    assert str(exc_info.value) == "Price must be a non-negative float."

# Prueba de creación de un Place con latitud fuera de rango
def test_create_place_invalid_latitude():
    with pytest.raises(ValueError) as exc_info:
        Place(title="Beach House", description="A lovely beach house.", price=150.0, latitude=100.0, longitude=-118.5, owner="John Doe")
    assert str(exc_info.value) == "Latitude must be between -90 and 90."

# Prueba de creación de un Place con longitud fuera de rango
def test_create_place_invalid_longitude():
    with pytest.raises(ValueError) as exc_info:
        Place(title="Beach House", description="A lovely beach house.", price=150.0, latitude=34.0, longitude=200.0, owner="John Doe")
    assert str(exc_info.value) == "Longitude must be between -180 and 180."

# Prueba de creación de un Place con propietario vacío
def test_create_place_empty_owner():
    with pytest.raises(ValueError) as exc_info:
        Place(title="Beach House", description="A lovely beach house.", price=150.0, latitude=34.0, longitude=-118.5, owner="")
    assert str(exc_info.value) == "Owner cannot be empty"
