import pytest
from app import create_app
from app.models import User

@pytest.fixture
def client():
    app = create_app()
    app.config.update({
        "TESTING": True
    })
    with app.test_client() as client:
        yield client

def test_create_user_valid():
    # Crear un usuario con datos válidos
    user = User("John", "Doe", "pepito.doe@example.com")
    assert user.first_name == "John"
    assert user.last_name == "Doe"
    assert user.email == "john.doe@example.com"
    assert user.is_admin is False

def test_create_user_invalid_email():
    # Crear un usuario con un email inválido
    with pytest.raises(ValueError) as excinfo:
        User("Jane", "Doe", "invalid-email")
    assert str(excinfo.value) == "Invalid email format"

def test_create_user_invalid_is_admin():
    # Crear un usuario con un valor incorrecto para is_admin
    with pytest.raises(ValueError) as excinfo:
        User("Jane", "Doe", "jane.doe@example.com", is_admin="yes")
    assert str(excinfo.value) == "is_admin must be a boolean"

def test_create_user_empty_first_name():
    # Crear un usuario con un primer nombre vacío
    with pytest.raises(ValueError) as excinfo:
        User("", "Doe", "john.doe@example.com")
    assert str(excinfo.value) == "First name cannot be empty"

def test_create_user_empty_last_name():
    # Crear un usuario con un apellido vacío
    with pytest.raises(ValueError) as excinfo:
        User("John", "", "john.doe@example.com")
    assert str(excinfo.value) == "Last name cannot be empty"

# Pruebas para la API REST

def test_create_user_api(client):
    response = client.post('/api/v1/users/', json={
        "first_name": "Jane",
        "last_name": "Doe",
        "email": "jane.doe@example.com"
    })
    assert response.status_code == 201
    assert response.json["first_name"] == "Jane"
    assert response.json["last_name"] == "Doe"
    assert response.json["email"] == "jane.doe@example.com"

def test_create_user_invalid_data_api(client):
    response = client.post('/api/v1/users/', json={
        "first_name": "",
        "last_name": "",
        "email": "invalid-email"
    })
    assert response.status_code == 400
    assert "error" in response.json
