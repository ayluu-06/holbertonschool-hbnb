from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask_jwt_extended import jwt_required

api = Namespace('amenities', description='Amenity operations')

amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity')
})

amenity_response_model = api.inherit('AmenityResponse', amenity_model, {
    'id': fields.String(description='Unique identifier of the amenity'),
    'created_at': fields.String(description='Creation timestamp'),
    'updated_at': fields.String(description='Last update timestamp')
})

@api.route('/')
class AmenityList(Resource):
    @jwt_required()
    @api.doc('list_amenities')
    @api.marshal_list_with(amenity_response_model)
    def get(self):
        amenities = facade.get_all_amenities()
        return [amenity.to_dict() for amenity in amenities]

    @api.doc('create_amenity')
    @api.expect(amenity_model, validate=True)
    @api.response(201, 'Amenity successfully created', amenity_response_model)
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new amenity"""
        amenity_data = api.payload

        try:
            new_amenity = facade.create_amenity(amenity_data)
            return new_amenity.to_dict(), 201
        except ValueError as e:
            api.abort(400, str(e))

@api.route('/<string:amenity_id>')
@api.param('amenity_id', 'The amenity identifier')
class AmenityResource(Resource):
    @jwt_required()
    @api.doc('get_amenity')
    @api.response(200, 'Success', amenity_response_model)
    @api.response(404, 'Amenity not found')
    def get(self, amenity_id):
        """Get amenity details by ID"""
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            api.abort(404, 'Amenity not found')
        return amenity.to_dict()

    @api.doc('update_amenity')
    @api.expect(amenity_model)
    @api.response(200, 'Amenity successfully updated', amenity_response_model)
    @api.response(404, 'Amenity not found')
    @api.response(400, 'Invalid input data')
    def put(self, amenity_id):
        """Update amenity details"""
        amenity_data = api.payload
        
        if not amenity_data.get('name'):
            api.abort(400, 'Name of the amenity is required')
        try:
            amenity = facade.update_amenity(amenity_id, amenity_data)
            if not amenity:
                api.abort(404, 'Amenity not found')
            return amenity.to_dict()
        except ValueError as e:
            api.abort(400, str(e))
