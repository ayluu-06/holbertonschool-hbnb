from flask import Flask
from flask_restx import Api
from hbnb.config import config
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

bcrypt = Bcrypt()
jwt = JWTManager()
db = SQLAlchemy()  # inicializo la instancia de SQLAlchemy
migrate = Migrate()

def create_app(config_class='development'):
    app = Flask(__name__)
    app.config.from_object(config[config_class])
    api = Api(app, version='1.0', title='HBnB API', description='HBnB Application API')
    
    bcrypt.init_app(app)
    jwt.init_app(app)
    db.init_app(app)  # inicializo sql alquemy con la app
    migrate.init_app(app, db)

    # importamos los namespaces dentro para evitar circular imports
    from app.api.v1.amenities import api as amenities_ns
    from app.api.v1.places import api as places_ns
    from app.api.v1.reviews import api as reviews_ns
    from app.api.v1.auth import api as auth_ns
    from app.api.v1.users import api as users_ns

    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(amenities_ns, path='/api/v1/amenities')
    api.add_namespace(places_ns, path='/api/v1/places')
    api.add_namespace(reviews_ns, path='/api/v1/reviews')
    api.add_namespace(auth_ns, path='/api/v1/auth')
    
    return app