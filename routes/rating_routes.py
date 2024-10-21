# routes/rating_routes.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.exc import SQLAlchemyError
from models import Rating, Movie, User
from database import db

rating_bp = Blueprint('rating', __name__)

# User: Add or update rating for a movie
@rating_bp.route('/<int:movie_id>/rate', methods=['POST', 'PUT'])
@jwt_required()
def rate_movie(movie_id):
    current_user = get_jwt_identity()
    if current_user['role'] == 'admin':
        return jsonify(message="Admins cannot rate movies"), 403

    movie = Movie.query.get(movie_id)
    if not movie:
        return jsonify(message="Movie not found"), 404

    data = request.get_json()
    rating_value = data['rating']
    review = data.get('review', '')

    rating = Rating.query.filter_by(movie_id=movie_id, user_id=current_user['id']).first()
    if rating:
        rating.rating = rating_value
        rating.review = review
    else:
        rating = Rating(movie_id=movie_id, user_id=current_user['id'], rating=rating_value, review=review)
        db.session.add(rating)

    db.session.commit()

    return jsonify(message="Rating submitted/updated successfully"), 201

# User: Delete their own rating
@rating_bp.route('/<int:movie_id>/rating/<int:rating_id>/delete', methods=['DELETE'])
@jwt_required()
def delete_own_rating(movie_id, rating_id):
    current_user = get_jwt_identity()

    rating = Rating.query.filter_by(id=rating_id, user_id=current_user['id']).first()
    if not rating:
        return jsonify(message="Rating not found"), 404

    db.session.delete(rating)
    db.session.commit()

    return jsonify(message="Your rating has been deleted"), 200

# Admin: Delete any rating
@rating_bp.route('/<int:movie_id>/rating/<int:rating_id>/delete/admin', methods=['DELETE'])
@jwt_required()
def delete_rating_admin(movie_id, rating_id):
    current_user = get_jwt_identity()
    if current_user['role'] != 'admin':
        return jsonify(message="Admins only!"), 403

    rating = Rating.query.get(rating_id)
    if not rating:
        return jsonify(message="Rating not found"), 404

    db.session.delete(rating)
    db.session.commit()

    return jsonify(message="Rating deleted successfully"), 200