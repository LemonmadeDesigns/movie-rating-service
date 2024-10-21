# routes/movie_routes.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from models import Movie
from sqlalchemy.exc import SQLAlchemyError

# Ensure the Blueprint is properly defined
movie_bp = Blueprint('movie', __name__)

@movie_bp.route('/movies', methods=['GET'])
def get_movies():
    # Dummy example: List of movies
    movies = [
        {'id': 1, 'title': 'The Matrix', 'release_year': 1999},
        {'id': 2, 'title': 'Inception', 'release_year': 2010},
    ]
    return jsonify(movies), 200

# Route to add a new movie (Admin only)
@movie_bp.route('/movies', methods=['POST'])
@jwt_required()
def add_movie():
    identity = get_jwt_identity()
    if identity['role'] != 'admin':
        return jsonify(message="Admin access required!"), 403
    
    data = request.get_json()
    try:
        title = data['title']
        description = data.get('description')
        release_year = data.get('release_year')

        new_movie = Movie(title=title, description=description, release_year=release_year)
        db.session.add(new_movie)
        db.session.commit()

        return jsonify(message="Movie added successfully!"), 201
    except KeyError:
        return jsonify(message="Missing required fields."), 400
    except SQLAlchemyError as e:
        db.session.rollback()  # Rollback in case of error
        return jsonify(message=f"Database error: {str(e)}"), 500
