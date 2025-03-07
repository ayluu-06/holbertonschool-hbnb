from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('users', description='User operations')

# Definir el modelo de usuario para validación y documentación
user_model = api.model('User', {
    'first_name': fields.String(required=True, description='Nombre del usuario'),
    'last_name': fields.String(required=True, description='Apellido del usuario'),
    'email': fields.String(required=True, description='Correo electrónico del usuario')
})

@api.route('/')
class UserList(Resource):
    @api.expect(user_model, validate=True)
    @api.response(201, 'Usuario creado exitosamente')
    @api.response(400, 'Correo ya registrado')
    @api.response(400, 'Datos de entrada inválidos')
    def post(self):
        """Registrar un nuevo usuario"""
        user_data = api.payload

        # Simulación de verificación de email único
        existing_user = facade.get_user_by_email(user_data['email'])
        if existing_user:
            return {'error': 'Correo ya registrado'}, 400

        new_user = facade.create_user(user_data)
        return {
            'id': new_user.id,
            'first_name': new_user.first_name,
            'last_name': new_user.last_name,
            'email': new_user.email
        }, 201

    @api.response(200, 'Lista de usuarios obtenida correctamente')
    @api.response(500, 'Error interno del servidor')
    def get(self):
        """Obtener todos los usuarios"""
        try:
            # Método que devuelve todos los usuarios
            users = facade.get_all_users()  
            return [{'id': user.id, 'first_name': user.first_name, 'last_name': user.last_name, 'email': user.email} for user in users], 200
        except Exception as e:
            return {'error': 'Error en el servidor', 'message': str(e)}, 500

@api.route('/<user_id>')
class UserResource(Resource):
    @api.response(200, 'Detalles del usuario obtenidos correctamente')
    @api.response(404, 'Usuario no encontrado')
    def get(self, user_id):
        """Obtener detalles del usuario por ID"""
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'Usuario no encontrado'}, 404

        return {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email
        }, 200
