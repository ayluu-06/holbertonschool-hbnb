from flask_restx import Namespace, Resource, fields
from flask_bcrypt import Bcrypt
from app.services import facade

api = Namespace('users', description='User operations')
bcrypt = Bcrypt()

# Modelo para validación
user_model = api.model('User', {
    'first_name': fields.String(required=True, description='User first name'),
    'last_name': fields.String(required=True, description='User last name'),
    'email': fields.String(required=True, description='User email'),
    'password': fields.String(required=True, description='User password')
})

# Función para hashear la contraseña
def hash_password(password):
    return bcrypt.generate_password_hash(password).decode('utf-8')

@api.route('/')
class UserList(Resource):
    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Email already registered')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new user"""
        user_data = api.payload

        # Verificar si el correo ya existe
        if facade.get_user_by_email(user_data['email']):
            return {'error': 'Email already registered'}, 400

        # Hashear la contraseña antes de guardar
        user_data['password'] = hash_password(user_data['password'])

        # Crear el usuario
        new_user = facade.create_user(user_data)

        # Respuesta sin la contraseña
        return {
            'id': new_user.id,
            'first_name': new_user.first_name,
            'last_name': new_user.last_name,
            'email': new_user.email
        }, 201

    @api.response(200, 'User list retrieved successfully')
    @api.response(500, 'Internal server error')
    def get(self):
        """Get all users"""
        try:
            users = facade.get_all_users()
            return [
                {
                    'id': user.id,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'email': user.email
                }
                for user in users
            ], 200
        except Exception as e:
            return {'error': 'Server error', 'message': str(e)}, 500

@api.route('/<user_id>')
class UserResource(Resource):
    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    @api.response(400, 'Invalid user ID')
    def get(self, user_id):
        """Get user details by ID"""
        if not user_id.isdigit():
            return {'error': 'Invalid user ID'}, 400

        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404

        return {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email
        }, 200
