import uuid
from datetime import datetime
from app import db

class BaseModel(db.Model):
    __abstract__ = True  # No se crea como tabla en la base de datos

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def save(self):
        #Guarda la instancia en la base de datos
        self.updated_at = datetime.utcnow()
        db.session.add(self)
        db.session.commit()

    def update(self, data):
        #Actualiza los atributos y guarda cambios
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.save()
