import unittest
from flask import Flask
from hbnb.app import create_app, db
from flask_jwt_extended import create_access_token

class UserTestCase(unittest.TestCase):
    def setUp(self):
        """Configuración inicial antes de cada prueba"""
        self.app = create_app("testing")  # Modo de pruebas
        self.client = self.app.test_client()
        self.access_token = create_access_token(identity={"id": "admin123", "is_admin": True})
        self.headers = {"Authorization": f"Bearer {self.access_token}"}

        # Activar el contexto manualmente para evitar errores de Flask
        self.app_context = self.app.app_context()
        self.app_context.push()

        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        """Se ejecuta después de cada prueba"""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
        
        # Cierra el contexto correctamente
        self.app_context.pop()

    def test_create_user(self):
        """Prueba la creación de usuario con autenticación"""
        response = self.client.post("/api/v1/users/", json={
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com"
        }, headers=self.headers)

        self.assertEqual(response.status_code, 201)
        
        # Validaciones más detalladas
        user_data = response.json
        self.assertIsInstance(user_data, dict)
        self.assertIn("id", user_data)
        self.assertEqual(user_data["email"], "john.doe@example.com")
        
        # Validar que el usuario realmente fue creado en la BD
        with self.app.app_context():
            user = db.session.get_user_by_email("john.doe@example.com")
            self.assertIsNotNone(user)

    def test_create_user_without_auth(self):
        #Prueba la creación de usuario sin autenticación
        response = self.client.post("/api/v1/users/", json={
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jane.doe@example.com"
        })

        self.assertEqual(response.status_code, 401)
        self.assertIn("msg", response.json)
        self.assertEqual(response.json["msg"], "Missing Authorization Header")

if __name__ == "__main__":
    unittest.main()
