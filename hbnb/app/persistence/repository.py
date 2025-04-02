# app/persistence/repository.py

import uuid
from datetime import datetime
import importlib
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity
from abc import ABC, abstractmethod

# Definir el repositorio base
class Repository(ABC):
    @abstractmethod
    def add(self, obj):
        pass

    @abstractmethod
    def get(self, obj_id):
        pass

    @abstractmethod
    def get_all(self):
        pass

    @abstractmethod
    def update(self, obj_id, data):
        pass

    @abstractmethod
    def delete(self, obj_id):
        pass

    @abstractmethod
    def get_by_attribute(self, attr_name, attr_value):
        pass


# Repositorio en memoria (para pruebas o almacenamiento temporal)
class InMemoryRepository(Repository):
    def __init__(self):
        self._storage = {}

    def add(self, obj):
        if not hasattr(obj, "id") or obj.id is None:
            obj.id = str(uuid.uuid4())
        if hasattr(obj, "created_at") and obj.created_at is None:
            obj.created_at = datetime.utcnow()
        if hasattr(obj, "updated_at") and obj.updated_at is None:
            obj.updated_at = datetime.utcnow()

        self._storage[obj.id] = obj

    def get(self, obj_id):
        return self._storage.get(obj_id)

    def get_all(self):
        return list(self._storage.values())

    def update(self, obj_id, data):
        obj = self.get(obj_id)
        if obj:
            for key, value in data.items():
                setattr(obj, key, value)
            obj.updated_at = datetime.utcnow()

    def delete(self, obj_id):
        if obj_id in self._storage:
            del self._storage[obj_id]

    def delete_all(self):
        confirmation = input("Are you sure you want to delete all items? (y/n): ")
        if confirmation.lower() == 'y':
            self._storage.clear()
            print("All items deleted.")

    def get_by_attribute(self, attr_name, attr_value):
        return next((obj for obj in self._storage.values() if getattr(obj, attr_name, None) == attr_value), None)


# Repositorio basado en SQLAlchemy
class SQLAlchemyRepository(Repository):
    def __init__(self, model, db_instance):
        self.model = model
        self.db = db_instance  # Usamos la instancia de db pasada

    def add(self, obj):
        try: 
            self.db.session.add(obj)
            self.db.session.commit()
        except Exception as e:
            self.db.session.rollback()  # Evita cambios no confirmados
            print(f"Error adding object: {e}")

    def get(self, obj_id):
        return self.model.query.get(obj_id)

    def get_all(self):
        return self.model.query.all()

    def update(self, obj_id, data):
        obj = self.get(obj_id)
        if obj:
            for key, value in data.items():
                setattr(obj, key, value)
            self.db.session.commit()

    def delete(self, obj_id):
        obj = self.get(obj_id)
        if obj:
            self.db.session.delete(obj)
            self.db.session.commit()

    def get_by_attribute(self, attr_name, attr_value):
        return self.model.query.filter_by(**{attr_name: attr_value}).first()


# Repositorio específico para el modelo de usuario
class UserRepository(SQLAlchemyRepository):
    def __init__(self, db_instance):
        super().__init__(User, db_instance)

    def create_user(self, first_name, last_name, email, password, is_admin=False):
        user = self.model(first_name=first_name, last_name=last_name, email=email, password=password, is_admin=is_admin)
        self.add(user)
        return user

    def get_user_by_id(self, user_id):
        return self.db.session.query(self.model).filter_by(id=user_id).first()

    def get_user_by_email(self, email):
        return self.db.session.query(self.model).filter_by(email=email).first()

    def update_user(self, user_id, first_name=None, last_name=None, email=None, is_admin=None):
        user = self.get_user_by_id(user_id)
        if user:
            if first_name is not None:
                user.first_name = first_name
            if last_name is not None:
                user.last_name = last_name
            if email is not None:
                user.email = email
            if is_admin is not None:
                user.is_admin = is_admin
            self.update(user_id, user.__dict__)
        return user

    def delete_user(self, user_id):
        user = self.get_user_by_id(user_id)
        if user:
            self.db.session.delete(user)
            self.db.session.commit()
            return True
        return False  # Indica que el usuario no existía



# Repositorio específico para el modelo de lugar
class PlaceRepository(SQLAlchemyRepository):
    def __init__(self, db_instance):
        super().__init__(Place, db_instance)

    def get_places_by_owner(self, owner_id):
        return self.model.query.filter_by(owner_id=owner_id).all()


# Repositorio específico para el modelo de reseña
class ReviewRepository(SQLAlchemyRepository):
    def __init__(self, db_instance):
        super().__init__(Review, db_instance)

    def get_reviews_by_place(self, place_id):
        return self.model.query.filter_by(place_id=place_id).all()


# Repositorio específico para el modelo de amenidad
class AmenityRepository(SQLAlchemyRepository):
    def __init__(self, db_instance):
        super().__init__(Amenity, db_instance)
