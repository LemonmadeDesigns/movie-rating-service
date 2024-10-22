# manage.py
from flask.cli import FlaskGroup
from app import create_app
from database import db
from models import User, Movie
from werkzeug.security import generate_password_hash
import click
from sqlalchemy.exc import IntegrityError

cli = FlaskGroup(create_app=create_app)

@cli.command("init-db")
def init_db():
    """Initialize the database."""
    with create_app().app_context():
        db.create_all()
        click.echo('Initialized the database.')

@cli.command("create-admin")
@click.argument("username")
@click.argument("password")
def create_admin(username, password):
    """Create an admin user."""
    with create_app().app_context():
        # Check if user already exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            if existing_user.role == 'admin':
                click.echo(f'Admin user {username} already exists.')
                return
            else:
                # Update existing user to admin
                existing_user.role = 'admin'
                existing_user.password = generate_password_hash(password)
                db.session.commit()
                click.echo(f'Updated existing user {username} to admin role.')
                return

        try:
            user = User(
                username=username,
                password=generate_password_hash(password),
                role='admin'
            )
            db.session.add(user)
            db.session.commit()
            click.echo(f'Created new admin user: {username}')
        except IntegrityError:
            db.session.rollback()
            click.echo(f'Error: Username {username} already exists.')

@cli.command("add-sample-movies")
def add_sample_movies():
    """Add sample movies to the database."""
    with create_app().app_context():
        # Check if movies already exist
        if Movie.query.first():
            click.echo('Movies already exist in the database.')
            return
            
        movies = [
            {
                'title': 'The Shawshank Redemption',
                'description': 'Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency.',
                'release_year': 1994
            },
            {
                'title': 'The Godfather',
                'description': 'The aging patriarch of an organized crime dynasty transfers control of his clandestine empire to his reluctant son.',
                'release_year': 1972
            },
            {
                'title': 'The Dark Knight',
                'description': 'When the menace known as the Joker wreaks havoc and chaos on the people of Gotham, Batman must accept one of the greatest psychological and physical tests of his ability to fight injustice.',
                'release_year': 2008
            }
        ]

        for movie_data in movies:
            movie = Movie(**movie_data)
            db.session.add(movie)
        
        db.session.commit()
        click.echo('Added sample movies to the database.')

@cli.command("reset-db")
def reset_db():
    """Reset the database (drop all tables and recreate)."""
    if click.confirm('Are you sure you want to reset the database? This will delete all data!'):
        with create_app().app_context():
            db.drop_all()
            db.create_all()
            click.echo('Database has been reset.')

if __name__ == '__main__':
    cli()