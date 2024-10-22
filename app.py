# app.py
import os
import psycopg2
from psycopg2 import sql
from flask import Flask, render_template
from flask_wtf.csrf import CSRFProtect
from config import Config
from flask_migrate import Migrate
from flask_login import LoginManager
from database import db
from models import User

# Initialize Flask extensions
csrf = CSRFProtect()
login_manager = LoginManager()
migrate = Migrate()

def create_database():
    """Creates the database if it doesn't exist."""
    db_name = 'movie_rating_service'
    user = 'postgres'
    password = 'postgres'
    host = 'localhost'

    try:
        connection = psycopg2.connect(
            dbname="postgres",
            user=user,
            password=password,
            host=host
        )
        connection.autocommit = True
        cursor = connection.cursor()
        cursor.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(db_name)))
        cursor.close()
        connection.close()
        print(f"Database '{db_name}' created successfully.")
    except psycopg2.errors.DuplicateDatabase:
        print(f"Database '{db_name}' already exists.")
    except Exception as e:
        print(f"Error creating database: {e}")

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    csrf.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    # Configure Flask-Login
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'info'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Register blueprints
    from routes.auth_routes import auth_bp
    from routes.movie_routes import movie_bp
    from routes.rating_routes import rating_bp
    from routes.file_upload import file_bp

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(movie_bp, url_prefix='/movies')
    app.register_blueprint(rating_bp, url_prefix='/ratings')
    app.register_blueprint(file_bp, url_prefix='/files')
    
    # Error handlers
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('errors/404.html'), 404

    @app.errorhandler(403)
    def forbidden_error(error):
        return render_template('errors/403.html'), 403

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return render_template('errors/500.html'), 500

    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)