import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')  # Asegúrate de tener esta variable de entorno
    DEBUG = False

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
