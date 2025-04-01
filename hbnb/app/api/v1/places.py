from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('places', description='Place operations / Operaciones de lugares')

# Define the models for related entities / Definir los modelos para entidades relacionadas
amenity_model = api.model('PlaceAmenity', {
    'id': fields.String(description='Amenity ID / ID de la amenidad'),
    'name': fields.String(description='Name of the amenity / Nombre de la amenidad')
})

user_model = api.model('PlaceUser', {
    'id': fields.String(description='User ID / ID del usuario'),
    'first_name': fields.String(description='First name of the owner / Nombre del propietario'),
    'last_name': fields.String(description='Last name of the owner / Apellido del propietario'),
    'email': fields.String(description='Email of the owner / Correo electrónico del propietario')
})

# Define the place model for input validation and documentation / Modelo de lugar para validación y documentación
place_model = api.model('Place', {
    'title': fields.String(required=True, description='Title of the place / Título del lugar'),
    'description': fields.String(description='Description of the place / Descripción del lugar'),
    'price': fields.Float(required=True, description='Price per night / Precio por noche'),
    'latitude': fields.Float(required=True, description='Latitude of the place / Latitud del lugar'),
    'longitude': fields.Float(required=True, description='Longitude of the place / Longitud del lugar'),
    'owner_id': fields.String(required=True, description='ID of the owner / ID del propietario'),
    'amenities': fields.List(fields.String, required=True, description="List of amenities ID's / Lista de ID de amenidades")
})

@api.route('/')
class PlaceList(Resource):
    @api.expect(place_model)
    @api.response(201, 'Place successfully created / Lugar creado con éxito')
    @api.response(400, 'Invalid input data / Datos de entrada inválidos')
    def post(self):
        """Register a new place / Registrar un nuevo lugar"""
        place_data = api.payload
        try:
            new_place = facade.create_place(place_data)  # Create place using facade / Crear el lugar usando la fachada
            return new_place, 201
        except ValueError as e:
            return {'error': str(e)}, 400

    @api.response(200, 'List of places retrieved successfully / Lista de lugares recuperada con éxito')
    def get(self):
        """Retrieve a list of all places / Obtener una lista de todos los lugares"""
        places = facade.get_all_places()
        return [place.to_dict() for place in places], 200  # Ensure each place is serialized / Asegurar que cada lugar se serialice

@api.route('/<place_id>')
class PlaceResource(Resource):
    @api.response(200, 'Place details retrieved successfully / Detalles del lugar recuperados con éxito')
    @api.response(404, 'Place not found / Lugar no encontrado')
    def get(self, place_id):
        """Get place details by ID / Obtener detalles de un lugar por ID"""
        place = facade.get_place(place_id)
        if place:
            return place.to_dict(), 200  # Return place as dictionary / Devolver el lugar como un diccionario
        return {'error': 'Place not found / Lugar no encontrado'}, 404

    @api.expect(place_model)
    @api.response(200, 'Place updated successfully / Lugar actualizado con éxito')
    @api.response(404, 'Place not found / Lugar no encontrado')
    @api.response(400, 'Invalid input data / Datos de entrada inválidos')
    def put(self, place_id):
        """Update a place's information / Actualizar la información de un lugar"""
        place_data = api.payload
        try:
            updated_place = facade.update_place(place_id, place_data)
            return updated_place.to_dict(), 200  # Return updated place as dictionary / Devolver el lugar actualizado como un diccionario
        except ValueError as e:
            return {'error': str(e)}, 400
