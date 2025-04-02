from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask_jwt_extended import jwt_required

# Espacio de nombres para las operaciones de reseñas
# Namespace for review operations
api = Namespace('reviews', description='Review operations')

# Modelo de datos para la validación de entrada y documentación
# Data model for input validation and documentation
review_model = api.model('Review', {
    'text': fields.String(required=True, description='Text of the review / Texto de la reseña'),
    'rating': fields.Integer(required=True, description='Rating of the place (1-5) / Calificación del lugar (1-5)'),
    'user_id': fields.String(required=True, description='ID of the user / ID del usuario'),
    'place_id': fields.String(required=True, description='ID of the place / ID del lugar')
})

@api.route('/')
class ReviewList(Resource):
    @jwt_required()
    @api.expect(review_model)
    @api.response(201, 'Review successfully created / Reseña creada exitosamente')
    @api.response(400, 'Invalid input data / Datos de entrada no válidos')
    def post(self):
        """Registrar una nueva reseña / Register a new review"""
        review_data = api.payload
        try:
            new_review = facade.create_review(review_data)
            return new_review, 201
        except ValueError as e:
            return {'error': str(e)}, 400

    @api.response(200, 'List of reviews retrieved successfully / Lista de reseñas recuperada exitosamente')
    def get(self):
        """Obtener todas las reseñas / Retrieve a list of all reviews"""
        reviews = facade.get_all_reviews()
        return [review.to_dict() for review in reviews], 200

@api.route('/<review_id>')
class ReviewResource(Resource):
    @api.response(200, 'Review details retrieved successfully / Detalles de la reseña recuperados exitosamente')
    @api.response(404, 'Review not found / Reseña no encontrada')
    def get(self, review_id):
        """Obtener detalles de una reseña por ID / Get review details by ID"""
        review = facade.get_review(review_id)
        if review:
            return review.to_dict(), 200
        return {'error': 'Review not found'}, 404

    @api.expect(review_model)
    @api.response(200, 'Review updated successfully / Reseña actualizada exitosamente')
    @api.response(404, 'Review not found / Reseña no encontrada')
    @api.response(400, 'Invalid input data / Datos de entrada no válidos')
    def put(self, review_id):
        """Actualizar la información de una reseña / Update a review's information"""
        review_data = api.payload
        try:
            updated_review = facade.update_review(review_id, review_data)
            return updated_review.to_dict(), 200
        except ValueError as e:
            return {'error': str(e)}, 400

    @api.response(200, 'Review deleted successfully / Reseña eliminada exitosamente')
    @api.response(404, 'Review not found / Reseña no encontrada')
    def delete(self, review_id):
        """Eliminar una reseña"""
        review = facade.get_review(review_id)  # Validar existencia antes de eliminar
        if not review:
            return {'error': 'Review not found'}, 404

        try:
            facade.delete_review(review_id)
            return {'message': 'Review deleted successfully'}, 200
        except Exception as e:
            return {'error': str(e)}, 400

@api.route('/places/<place_id>/reviews')
class PlaceReviewList(Resource):
    @api.response(200, 'List of reviews for the place retrieved successfully / Lista de reseñas del lugar recuperada exitosamente')
    @api.response(404, 'Place not found / Lugar no encontrado')
    def get(self, place_id):
        """Obtener todas las reseñas de un lugar específico / Get all reviews for a specific place"""
        reviews = facade.get_reviews_by_place(place_id)
        if reviews:
            return [review.to_dict() for review in reviews], 200
        return {'error': 'Place not found'}, 404
