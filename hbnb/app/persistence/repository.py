from datetime import datetime
import uuid
from app import db
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity
from abc import ABC, abstractmethod
from datetime import datetime
import uuid

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

        self._storage[obj.id] = obj  # Guardar el objeto en el almacenamiento en memoria

    def get(self, obj_id):
        return self._storage.get(obj_id)

    def get_all(self):
        return list(self._storage.values())

    def update(self, obj_id, data):
        obj = self.get(obj_id)
        if obj:
            # Actualizar todos los atributos del objeto (no solo los predefinidos)
            for key, value in data.items():
                setattr(obj, key, value)
            obj.updated_at = datetime.utcnow()  # Actualizar la fecha de modificación

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


    def get_by_id(self, obj_id):
        return self.get(obj_id)

class SQLAlchemyRepository(Repository):
    def __init__(self, model):
        self.model = model

    def add(self, obj):
        db.session.add(obj)
        db.session.commit()

    def get(self, obj_id):
        return self.model.query.get(obj_id)

    def get_all(self):
        return self.model.query.all()

    def update(self, obj_id, data):
        obj = self.get(obj_id)
        if obj:
            for key, value in data.items():
                setattr(obj, key, value)
            db.session.commit()

    def delete(self, obj_id):
        obj = self.get(obj_id)
        if obj:
            db.session.delete(obj)
            db.session.commit()

    def get_by_attribute(self, attr_name, attr_value):
        return self.model.query.filter_by(**{attr_name: attr_value}).first()

class UserRepository(SQLAlchemyRepository):
    def __init__(self):
        self.model = User

    def create_user(self, first_name, last_name, email, password, is_admin=False):
        user = self.model(first_name=first_name, last_name=last_name, email=email, password=password, is_admin=is_admin)
        self.add(user)
        return user

    def get_user_by_id(self, user_id):
        return db.session.query(self.model).filter_by(id=user_id).first()

    def get_user_by_email(self, email):
        return db.session.query(self.model).filter_by(email=email).first()

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
        user = self.get(user_id)
        if user:
            self.delete(user_id)
        return user

class PlaceRepository(SQLAlchemyRepository):
    def __init__(self):
        super().__init__(Place)

    def get_places_by_owner(self, owner_id):
        return self.model.query.filter_by(owner_id=owner_id).all()

class ReviewRepository(SQLAlchemyRepository):
    def __init__(self):
        super().__init__(Review)

    def get_reviews_by_place(self, place_id):
        return self.model.query.filter_by(place_id=place_id).all()

class AmenityRepository(SQLAlchemyRepository):
    def __init__(self):
        super().__init__(Amenity)
