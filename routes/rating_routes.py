# routes/rating_routes.py
from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from forms import RatingForm
from models import Rating, Movie
from database import db

rating_bp = Blueprint('ratings', __name__)

@rating_bp.route('/<int:movie_id>/rate', methods=['GET', 'POST'])
@login_required
def rate_movie(movie_id):
    if current_user.role == 'admin':
        flash('Admins cannot rate movies.', 'warning')
        return redirect(url_for('movie.get_movies'))
    
    movie = Movie.query.get_or_404(movie_id)
    form = RatingForm()
    
    # Check if user has already rated this movie
    existing_rating = Rating.query.filter_by(
        movie_id=movie_id,
        user_id=current_user.id
    ).first()
    
    if existing_rating:
        form.rating.data = existing_rating.rating
        form.review.data = existing_rating.review
    
    if form.validate_on_submit():
        if existing_rating:
            existing_rating.rating = form.rating.data
            existing_rating.review = form.review.data
            flash('Your rating has been updated!', 'success')
        else:
            rating = Rating(
                movie_id=movie_id,
                user_id=current_user.id,
                rating=form.rating.data,
                review=form.review.data
            )
            db.session.add(rating)
            flash('Your rating has been submitted!', 'success')
        
        db.session.commit()
        return redirect(url_for('movie.get_movies'))
    
    return render_template('rate_movie.html', form=form, movie=movie)

@rating_bp.route('/<int:movie_id>/rating/<int:rating_id>/delete', methods=['POST'])
@login_required
def delete_rating(movie_id, rating_id):
    rating = Rating.query.get_or_404(rating_id)
    
    if current_user.role != 'admin' and current_user.id != rating.user_id:
        flash('You cannot delete this rating.', 'danger')
        return redirect(url_for('movie.get_movies'))
    
    db.session.delete(rating)
    db.session.commit()
    flash('Rating deleted successfully!', 'success')
    return redirect(url_for('movie.get_movies'))