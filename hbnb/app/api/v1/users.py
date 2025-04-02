from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services import facade


api = Namespace('users', description='Operaciones con usuarios')

# Definir el modelo de usuario para validación y documentación
user_model = api.model('User', {
    'first_name': fields.String(required=True, description='Nombre del usuario'),
    'last_name': fields.String(required=True, description='Apellido del usuario'),
    'email': fields.String(required=True, description='Correo electrónico del usuario')
})

@api.route('/')
class UserList(Resource):
    @jwt_required()
    def post(self):
        """Registrar un nuevo usuario (solo administradores)"""
        current_user = get_jwt_identity()
        if not current_user.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403

        user_data = api.payload
       
        existing_user = facade.get_user_by_email(user_data['email'])
        if existing_user:
            return {'error': 'Correo ya registrado'}, 400

        new_user = facade.create_user(user_data)
        
        if not user_data.get('email'):
            return {'error': 'El correo electrónico es obligatorio'}, 400

        if not user_data.get('first_name'):
            return {'error': 'El nombre es obligatorio'}, 400

        if not user_data.get('last_name'):
            return {'error': 'El apellido es obligatorio'}, 400
        
        return new_user.to_dict(), 201
    

@api.route('/<user_id>')
class UserResource(Resource):
    @jwt_required()
    def put(self, user_id):
        """Modificar usuario (solo administradores o el mismo usuario)"""
        current_user = get_jwt_identity()
        is_admin = current_user.get('is_admin', False)
        user_id_from_token = current_user.get('id')

        if not is_admin and user_id != user_id_from_token:
            return {'error': 'Unauthorized action'}, 403

        user_data = api.payload
        email = user_data.get('email')

        if email:
            existing_user = facade.get_user_by_email(email)
            if existing_user and existing_user.id != user_id:
                return {'error': 'Correo ya en uso'}, 400

        updated_user = facade.update_user(user_id, user_data)
        return updated_user.to_dict(), 200
