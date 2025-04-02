from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask_jwt_extended import create_access_token, jwt_required

api = Namespace('users', description='User operations / Operaciones con usuarios')

# Define the user model for validation and documentation
# Definir el modelo de usuario para validación y documentación
user_model = api.model('User', {
    'first_name': fields.String(required=True, description="Users first name / Nombre del usuario"),
    'last_name': fields.String(required=True, description="Users last name / Apellido del usuario"),
    'email': fields.String(required=True, description="Users email / Correo electrónico del usuario")
})

@api.route('/')
class UserList(Resource):
    @jwt_required()
    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created / Usuario creado exitosamente')
    @api.response(400, 'Email already registered / Correo ya registrado')
    @api.response(400, 'Invalid input data / Datos de entrada inválidos')
    def post(self):
        """Register a new user / Registrar un nuevo usuario"""
        user_data = api.payload

        if not user_data.get('email') or not user_data.get('email').strip():
            return {'error': 'El correo electrónico es obligatorio'}, 400
        if not user_data.get('first_name') or not user_data.get('first_name').strip():
            return {'error': 'El nombre es obligatorio'}, 400
        if not user_data.get('last_name') or not user_data.get('last_name').strip():
            return {'error': 'El apellido es obligatorio'}, 400
        
        existing_user = facade.get_user_by_email(user_data['email'])
        if existing_user:
            return {'error': 'Email already registered / Correo ya registrado'}, 400

        new_user = facade.create_user(user_data)
        access_token = create_access_token(identity={'id': new_user.id, 'is_admin': new_user.is_admin})
        return {'access_token': access_token, 'user': new_user.to_dict()}, 201


@api.route('/<user_id>')
class UserResource(Resource):
    @jwt_required()
    @api.response(200, 'User details retrieved successfully / Detalles del usuario obtenidos correctamente')
    @api.response(404, 'User not found / Usuario no encontrado')
    def get(self, user_id):
        """Get user details by ID / Obtener detalles del usuario por ID"""
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found / Usuario no encontrado'}, 404

        return {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email
        }, 200
