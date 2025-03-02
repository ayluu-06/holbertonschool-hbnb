import pytest
from app.models.place import Place
from app.models.user import User
from app.models.review import Review

@pytest.fixture
def setup_place_and_user():
    # Creación de un Place y un User de prueba
    place = Place(title="Cozy Apartment", description="A nice place", price=100, latitude=37.7749, longitude=-122.4194, owner="John Doe")
    user = User(first_name="John", last_name="Doe", email="john.doe@example.com")
    return place, user

def test_review_text_too_short(setup_place_and_user):
    place, user = setup_place_and_user
    
    with pytest.raises(ValueError) as excinfo:
        Review(text="Short", rating=5, place=place, user=user)
    
    assert "Text must be at least 10 characters long" in str(excinfo.value)

def test_invalid_rating_low(setup_place_and_user):
    place, user = setup_place_and_user
    
    with pytest.raises(ValueError) as excinfo:
        Review(text="This place is good", rating=0, place=place, user=user)
    
    assert "Rating must be between 1 and 5" in str(excinfo.value)

def test_invalid_rating_high(setup_place_and_user):
    place, user = setup_place_and_user
    
    with pytest.raises(ValueError) as excinfo:
        Review(text="This place is good", rating=6, place=place, user=user)
    
    assert "Rating must be between 1 and 5" in str(excinfo.value)

def test_invalid_place(setup_place_and_user):
    place, user = setup_place_and_user
    invalid_place = "Not a place"
    
    with pytest.raises(ValueError) as excinfo:
        Review(text="This place is good", rating=5, place=invalid_place, user=user)
    
    assert "Place must be an instance of the Place class" in str(excinfo.value)

def test_invalid_user(setup_place_and_user):
    place, user = setup_place_and_user
    invalid_user = "Not a user"
    
    with pytest.raises(ValueError) as excinfo:
        Review(text="This place is good", rating=5, place=place, user=invalid_user)
    
    assert "User must be an instance of the User class" in str(excinfo.value)
