import os

class Config:
    DEBUG = False
    SECRET_KEY = os.environ.get("SECRET_KEY", "valor_por_defecto")
    DATABASE_URI = os.environ.get("DATABASE_URI", "sqlite:///fallback.db")
    FLASK_ENV = os.environ.get("FLASK_ENV", "development")

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv('DEV_DATABASE_URI', 'sqlite:///development.db')  # Configura tu URI desde la variable de entorno
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://user:password@localhost/dbname')  # Usa la URL de conexión para producción

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,  # Configuración para producción
    'default': DevelopmentConfig
}

class TestingConfig:
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig,
}