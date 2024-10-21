# routes/rating_routes.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.exc import SQLAlchemyError
from models import Movie, Rating

rating_bp = Blueprint('rating', __name__)

@rating_bp.route('/ratings', methods=['GET'])
def get_ratings():
    # Dummy example: List of ratings
    ratings = [
        {'id': 1, 'movie_id': 1, 'rating': 5, 'review': 'Excellent'},
        {'id': 2, 'movie_id': 2, 'rating': 4, 'review': 'Very Good'},
    ]
    return jsonify(ratings), 200

# User route to submit a rating for a movie
@rating_bp.route('/ratings', methods=['POST'])
@jwt_required()
def submit_rating():
    from app import db  # Local import to avoid circular dependency
    identity = get_jwt_identity()
    user_id = identity['id']
    
    data = request.get_json()
    try:
        movie_id = data['movie_id']
        rating_value = data['rating']
        review = data.get('review', '')

        movie = Movie.query.get(movie_id)
        if not movie:
            return jsonify(message="Movie not found."), 404
        
        # Check if the user has already rated this movie
        existing_rating = Rating.query.filter_by(user_id=user_id, movie_id=movie_id).first()
        if existing_rating:
            return jsonify(message="You have already rated this movie."), 400
        
        new_rating = Rating(movie_id=movie_id, user_id=user_id, rating=rating_value, review=review)
        db.session.add(new_rating)
        db.session.commit()

        return jsonify(message="Rating submitted successfully!"), 201
    except KeyError:
        return jsonify(message="Missing required fields."), 400
    except SQLAlchemyError as e:
        return jsonify(message=f"Database error: {str(e)}"), 500
