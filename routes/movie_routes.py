# routes/movie_routes.py
from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from database import db
from models import Movie
from forms import MovieForm

# Change the blueprint name to match what's in your templates
movie_bp = Blueprint('movie', __name__)

@movie_bp.route('/')
@login_required
def get_movies():
    movies = Movie.query.all()
    print(f"Current user: {current_user.username}")
    print(f"Current user role: {current_user.role}")
    return render_template('movies.html', movies=movies)

@movie_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_movie():
    if current_user.role != 'admin':
        flash('Access denied. Admin privileges required.', 'danger')
        return redirect(url_for('movie.get_movies'))
    
    form = MovieForm()
    if form.validate_on_submit():
        movie = Movie(
            title=form.title.data,
            description=form.description.data,
            release_year=form.release_year.data
        )
        db.session.add(movie)
        db.session.commit()
        flash('Movie added successfully!', 'success')
        return redirect(url_for('movie.get_movies'))
    
    return render_template('add_movie.html', form=form)

@movie_bp.route('/edit/<int:movie_id>', methods=['GET', 'POST'])
@login_required
def edit_movie(movie_id):
    if current_user.role != 'admin':
        flash('Access denied. Admin privileges required.', 'danger')
        return redirect(url_for('movie.get_movies'))
    
    movie = Movie.query.get_or_404(movie_id)
    form = MovieForm(obj=movie)
    
    if form.validate_on_submit():
        movie.title = form.title.data
        movie.description = form.description.data
        movie.release_year = form.release_year.data
        db.session.commit()
        flash('Movie updated successfully!', 'success')
        return redirect(url_for('movie.get_movies'))
    
    return render_template('edit_movie.html', form=form, movie=movie)

@movie_bp.route('/delete/<int:movie_id>', methods=['POST'])
@login_required
def delete_movie(movie_id):
    if current_user.role != 'admin':
        flash('Access denied. Admin privileges required.', 'danger')
        return redirect(url_for('movie.get_movies'))
    
    movie = Movie.query.get_or_404(movie_id)
    db.session.delete(movie)
    db.session.commit()
    flash('Movie deleted successfully!', 'success')
    return redirect(url_for('movie.get_movies'))

@movie_bp.route('/test-404')
def test_404():
    abort(404)

@movie_bp.route('/movie/<int:movie_id>')
def get_movie(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    return render_template('movie_detail.html', movie=movie)

@movie_bp.route('/test-500')
def test_500():
    raise Exception("Test 500 error")