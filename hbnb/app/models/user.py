#!/usr/bin/python3

"""Class User"""

import uuid
from app.models.base_model import BaseModel
from email_validator import validate_email, EmailNotValidError
from sqlalchemy.orm import validates
from app import bcrypt, db


class User(BaseModel):
    """Class User, inherits from BaseModel
    Clase User, hereda de BaseModel"""
    __tablename__ = 'users'
   
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    places = db.relationship('Place', backref='user', lazy=True, cascade='all, delete-orphan')
    reviews = db.relationship('Review', backref='user', lazy=True, cascade='all, delete-orphan')

    def __init__(self, first_name: str, last_name: str, email: str, password: str, is_admin: bool = False):
        #Initialize User with valid data
        #Inicializa el Usuario

        super().__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')
        self.is_admin = is_admin

    @validates('first_name')
    def validate_first_name(self, key, value):
        #Ensure first name is valid
        #Asegura que el primer nombre sea válido
        if not value or len(value) > 50:
            raise ValueError("First name is required and cannot exceed 50 characters")
            # El primer nombre es obligatorio y no puede superar los 50 caracteres
        return value

    @validates('last_name')
    def validate_last_name(self, key, value):
        #Ensure last name is valid
        #Asegura que el apellido sea válido
        if not value or len(value) > 50:
            raise ValueError("Last name is required and cannot exceed 50 characters")
            # El apellido es obligatorio y no puede superar los 50 caracteres
        return value

    @validates('email')
    def validate_email(self, key, value):
        """Validate and normalize email
        Valida y normaliza el correo electrónico"""
        try:
            email_info = validate_email(value, check_deliverability=False)
            return email_info.normalized 
            # Save normalized email
            # Guarda el correo electrónico normalizado
        except EmailNotValidError as e:
            raise ValueError(f"Invalid email: {e}")
            # Lanza un error si el correo no es válido
    
    @validates('password')
    def validate_password(self, key, value):
        if len(value) < 8:
            raise ValueError("La contraseña debe tener al menos 8 caracteres")
        return bcrypt.generate_password_hash(value).decode('utf-8')
    
    def verify_password(self, password):
        """Check if provided password matches stored password
        Verifica si la contraseña proporcionada coincide con la almacenada"""
        return bcrypt.check_password_hash(self.password, password)
