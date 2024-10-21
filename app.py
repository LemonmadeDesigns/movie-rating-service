# # app.py
# import psycopg2
# from psycopg2 import sql
# from flask import Flask, jsonify
# from flask_wtf.csrf import CSRFProtect
# from flask_jwt_extended import JWTManager
# from config import Config
# from flask_migrate import Migrate
# from database import db  # Import from the new database.py
# from routes.auth_routes import auth_bp

# migrate = Migrate()
# app = Flask(__name__)

# # Set a secret key for signing JWT tokens
# app.config['JWT_SECRET_KEY'] = 'your_secret_key'  # Use an environment variable in production
# csrf = CSRFProtect(app)


# def create_database():
#     """Creates the database if it doesn't exist."""
#     db_name = 'movie_rating_service'
#     user = 'postgres'
#     password = 'postgres'
#     host = 'localhost'

#     try:
#         # Connect to the default database to create the new one
#         connection = psycopg2.connect(
#             dbname="postgres",  # Connect to the default postgres database
#             user=user,
#             password=password,
#             host=host
#         )
#         connection.autocommit = True  # Ensure that the CREATE DATABASE command runs immediately

#         cursor = connection.cursor()

#         # Use SQL to create the database
#         cursor.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(db_name)))

#         cursor.close()
#         connection.close()

#         print(f"Database '{db_name}' created successfully.")

#     except psycopg2.errors.DuplicateDatabase:
#         print(f"Database '{db_name}' already exists.")
#     except Exception as e:
#         print(f"Error creating database: {e}")

# def create_app():
#     app = Flask(__name__)
#     app.config.from_object(Config)

#     # Initialize extensjwtions
#     db.init_app(app)
#     migrate.init_app(app, db)  # Initialize migration with the app and db
#     jwt.init_app(app)

#      # Create the database if it doesn't exist
#     create_database()
    
#     @app.before_request
#     def create_tables():
#         db.create_all()
        
#     # Define a simple root route
#     @app.route('/')
#     def home():
#         return jsonify(message="Welcome to the Movie Rating API"), 200

#     # Import and register blueprints
#     from routes.movie_routes import movie_bp
#     from routes.rating_routes import rating_bp
#     from routes.file_upload import file_bp
#     from routes.auth_routes import auth_bp

#     app.register_blueprint(movie_bp)
#     app.register_blueprint(rating_bp)
#     app.register_blueprint(file_bp)
#     app.register_blueprint(auth_bp)

#     return app

# if __name__ == '__main__':
#     app = create_app()
#     app.run(debug=True)


import psycopg2
from psycopg2 import sql
from flask import Flask, jsonify
from flask_wtf.csrf import CSRFProtect
from flask_jwt_extended import JWTManager
from config import Config
from flask_migrate import Migrate
from database import db  # Import from the new database.py

# Initialize Flask extensions
migrate = Migrate()
csrf = CSRFProtect()  # CSRF protection for forms
jwt = JWTManager()    # JWT manager for handling tokens

def create_database():
    """Creates the database if it doesn't exist."""
    db_name = 'movie_rating_service'
    user = 'postgres'
    password = 'postgres'
    host = 'localhost'

    try:
        # Connect to the default database to create the new one
        connection = psycopg2.connect(
            dbname="postgres",  # Connect to the default postgres database
            user=user,
            password=password,
            host=host
        )
        connection.autocommit = True  # Ensure that the CREATE DATABASE command runs immediately

        cursor = connection.cursor()

        # Use SQL to create the database
        cursor.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(db_name)))

        cursor.close()
        connection.close()

        print(f"Database '{db_name}' created successfully.")

    except psycopg2.errors.DuplicateDatabase:
        print(f"Database '{db_name}' already exists.")
    except Exception as e:
        print(f"Error creating database: {e}")

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)  # Load configurations from Config

    # Secret key required for WTForms CSRF protection
    app.config['SECRET_KEY'] = 'your_secret_key'  # Replace with an environment variable in production

    # Initialize extensions
    db.init_app(app)        # Initialize SQLAlchemy
    migrate.init_app(app, db)  # Initialize migration with the app and db
    csrf.init_app(app)       # Enable CSRF protection
    jwt.init_app(app)        # Initialize JWT manager

    # Create the database if it doesn't exist
    create_database()

    @app.before_request
    def create_tables():
        db.create_all()  # Automatically create database tables before each request
    
    # Define a simple root route
    @app.route('/')
    def home():
        return jsonify(message="Welcome to the Movie Rating API"), 200

    # Import and register blueprints
    from routes.movie_routes import movie_bp
    from routes.rating_routes import rating_bp
    from routes.file_upload import file_bp
    from routes.auth_routes import auth_bp

    app.register_blueprint(movie_bp)
    app.register_blueprint(rating_bp)
    app.register_blueprint(file_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')  # Add a URL prefix for auth routes
    # app.register_blueprint(auth_bp)  # Add a URL prefix for auth routes


    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
