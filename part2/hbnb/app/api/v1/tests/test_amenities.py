import pytest
from hbnb.run import create_app

@pytest.fixture
def client():
    """Configura el cliente de pruebas"""
    app = create_app()
    return app.test_client()

def test_create_user(client):
    """Prueba la creación de un usuario"""
    response = client.post('/api/v1/users/', json={
        "first_name": "Jane",
        "last_name": "Doe",
        "email": "jane.doe@example.com"
    })
    assert response.status_code == 201  # Verifica que el código de respuesta es 201 (Creado)

def test_create_user_invalid_data(client):
    """Prueba la creación de un usuario con datos inválidos"""
    response = client.post('/api/v1/users/', json={
        "first_name": "",
        "last_name": "",
        "email": "invalid-email"
    })
    assert response.status_code == 400