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
