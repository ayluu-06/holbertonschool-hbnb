import pytest
from app.models import User

def test_create_user_valid():
    # Crear un usuario con datos válidos
    user = User("John", "Doe", "john.doe@example.com")
    assert user.first_name == "John"
    assert user.last_name == "Doe"
    assert user.email == "john.doe@example.com"
    assert user.is_admin == False

def test_create_user_invalid_email():
    # Crear un usuario con un email inválido
    with pytest.raises(ValueError) as excinfo:
        User("Jane", "Doe", "invalid-email")
    assert str(excinfo.value) == "Invalid email format"

def test_create_user_invalid_is_admin():
    # Crear un usuario con un valor no adecuado para admin
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