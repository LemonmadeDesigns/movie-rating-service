# routes/movie_routes.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from database import db
from models import Movie
from sqlalchemy.exc import SQLAlchemyError

# Ensure the Blueprint is properly defined
movie_bp = Blueprint('movie', __name__)

# Admin: Add movie
@movie_bp.route('/add', methods=['POST'])
@jwt_required()
def add_movie():
    current_user = get_jwt_identity()
    if current_user['role'] != 'admin':
        return jsonify(message="Admins only!"), 403

    data = request.get_json()
    title = data['title']
    description = data.get('description', '')
    release_year = data.get('release_year')

    movie = Movie(title=title, description=description, release_year=release_year)
    db.session.add(movie)
    db.session.commit()

    return jsonify(message="Movie added successfully"), 201

# Fetch movie details and its ratings
@movie_bp.route('/<int:movie_id>', methods=['GET'])
@jwt_required()
def get_movie_details(movie_id):
    movie = Movie.query.get(movie_id)
    if not movie:
        return jsonify(message="Movie not found"), 404

    ratings = [{
        'user': rating.user.username,
        'rating': rating.rating,
        'review': rating.review
    } for rating in movie.ratings]

    return jsonify({
        'title': movie.title,
        'description': movie.description,
        'release_year': movie.release_year,
        'ratings': ratings
    }), 200