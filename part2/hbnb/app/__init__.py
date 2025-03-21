from flask import Flask
from flask_bcrypt import Bcrypt
from flask_restx import Api
from flask_cors import CORS
from app.api.v1.users import api as users_ns
from app.api.v1.amenities import api as amenities_ns
from app.api.v1.places import api as places_ns
from app.api.v1.reviews import api as reviews_ns
from flask_jwt_extended import JWTManager


def create_app(config_class=None):
    app = Flask(__name__)
    app.config['JWT_SECRET_KEY'] = 'my_super_secret_key'  # Clave secreta para generar tokens
    
    bcrypt = Bcrypt(app)
    jwt = JWTManager(app)

    # Cargar la configuración por defecto desde la clase
    if config_class:
        app.config.from_object(config_class)
    else:
        from config import DevelopmentConfig
        app.config.from_object(DevelopmentConfig)
    
    

    # Inicializa Flask-REST y CORS
    api = Api(app, version='1.0', title='HBnB API', description='HBnB Application API')
    CORS(app)

    # Registra los namespaces
    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(amenities_ns, path='/api/v1/amenities')
    api.add_namespace(places_ns, path='/api/v1/places')
    api.add_namespace(reviews_ns, path='/api/v1/reviews')

    return app
