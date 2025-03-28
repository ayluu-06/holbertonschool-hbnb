#!/usr/bin/python3
import bcrypt
from app.models.base_model import BaseModel
import re

class User(BaseModel):
    def __init__(self, first_name, last_name, email, is_admin=False):
        super().__init__()
        self.first_name = first_name
        self.lastname = last_name
        self.email = email
        self.is_admin = is_admin

        #funcion para validar el email
    def _is_valid_email(self, email):
        email_regex = r"(^[a-z0-9]+[.-_]*[a-z0-9]+@[a-z0-9-]+\.[a-z0-9-.]+$)"
        return re.match(email_regex, email) is not None
        
        #Funcion que cifra la contraseña antes de almacenarla.
    def hash_password(self, password):
        if not password:
            raise ValueError("Password cannot be empty")
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        #Verifica si la contraseña coincide con la almacenada.
    def verify_password(self, password):
        if not self.password_hash:
            raise ValueError("No password set for this user")
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))
