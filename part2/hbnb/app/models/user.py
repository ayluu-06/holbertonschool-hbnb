#!/usr/bin/python3

from app.models.base_model import BaseModel
import re

class User(BaseModel):
    def __init__(self, first_name, last_name, email, is_admin=False):
        super().__init__()

        # Validación del primer nombre
        if not first_name:
            raise ValueError("First name cannot be empty")
        self.first_name = first_name

        # Validación del apellido
        if not last_name:
            raise ValueError("Last name cannot be empty")
        self.last_name = last_name

        # Validación del email
        if not email:
            raise ValueError("Email cannot be empty")
        if not self._is_valid_email(email):
            raise ValueError("Invalid email format")
        self.email = email

        # Validación de si es admin
        if not isinstance(is_admin, bool):
            raise ValueError("is_admin must be a boolean")
        self.is_admin = is_admin

        #funcion para validar el email
    def _is_valid_email(self, email):
        email_regex = r"(^[a-z0-9]+[.-_]*[a-z0-9]+@[a-z0-9-]+\.[a-z0-9-.]+$)"
        return re.match(email_regex, email) is not None