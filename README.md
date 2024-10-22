# Movie Rating Service

This project is a **Movie Rating Service** built with Flask. It allows users to register, authenticate, view movies, and submit ratings. The service includes role-based access control (admin/user) and a clean web interface.

## Project Features

### 1. User Authentication & Authorization

- **User Registration**: Users can sign up with username and password
- **User Login**: Session-based authentication with Flask-Login
- **Role-Based Access**: Different functionalities for admin and regular users
- **User Session Management**: Secure login/logout functionality

### 2. Movie Management (Admin Only)

- **Add Movies**: Admins can add new movies with title, description, and release year
- **Edit Movies**: Admins can modify existing movie details
- **Delete Movies**: Admins can remove movies from the database
- **View All Movies**: Comprehensive movie listing with management options

### 3. User Rating System

- **Submit Ratings**: Regular users can rate movies (1-5 stars) and add reviews
- **View Ratings**: Users can see all movie ratings
- **Update Ratings**: Users can modify their own ratings
- **Delete Ratings**: Users can remove their own ratings

### 4. File Upload Support

- Restricted file upload functionality supporting specific extensions (png, jpg, jpeg, gif)
- Secure file handling and storage

## Technology Stack

- **Backend**: Flask (Python)
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Frontend**: Bootstrap 5, HTML templates with Jinja2
- **Authentication**: Flask-Login
- **Forms**: Flask-WTF
- **Security**: CSRF protection, password hashing
- **Environment**: Virtualenv for dependency management

## Installation Guide

1. Clone the repository:

   ```bash
   git clone https://github.com/LemonmadeDesigns/movie-rating-service.git
   cd movie-rating-service
   ```

2. Create and activate virtual environment:

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # For Linux/Mac
   venv\Scripts\activate     # For Windows
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Set up PostgreSQL database:

   ```bash
   psql postgres
   CREATE DATABASE movie_rating_service;
   \q
   ```

5. Initialize the database and create admin user:

   ```bash
   export FLASK_APP=app.py
   export FLASK_ENV=development
   
   # Initialize database tables
   flask db init
   flask db migrate -m "initial schema"
   flask db upgrade
   
   # Create admin user and add sample data
   python manage.py init-db
   python manage.py create-admin admin password123
   python manage.py add-sample-movies
   ```

6. Run the application:

   ```bash
   python app.py
   ```

7. Access the application at `http://localhost:5000`

## Available Routes

### User Authentication

- `/auth/register` - User registration
- `/auth/login` - User login
- `/auth/logout` - User logout

### Movie Management

- `/movies/` - View all movies
- `/movies/add` - Add new movie (admin only)
- `/movies/edit/<id>` - Edit movie (admin only)
- `/movies/delete/<id>` - Delete movie (admin only)

### Rating System

- `/ratings/<movie_id>/rate` - Rate a movie
- `/ratings/<movie_id>/rating/<rating_id>/delete` - Delete rating

### File Upload

- `/files/upload` - Upload files with restricted extensions

## User Roles

### Admin Users

- Can add, edit, and delete movies
- Cannot submit ratings
- Can view all movies and ratings
- Can delete any rating

### Regular Users

- Can view all movies
- Can submit, edit, and delete their own ratings
- Cannot modify movie information

## Database Schema

### Users

- id (Primary Key)
- username (Unique)
- password (Hashed)
- role (admin/user)
- active (Boolean)
- created_at (Timestamp)

### Movies

- id (Primary Key)
- title
- description
- release_year
- created_at (Timestamp)

### Ratings

- id (Primary Key)
- movie_id (Foreign Key)
- user_id (Foreign Key)
- rating (1-5)
- review (Text)
- created_at (Timestamp)

## Contributors

- **[Terrell D Lemons](LemonsTerrell@csu.fullerton.edu)** (CWID: 886659440)
- **[Kyle Williams](Kyle.williams953@csu.fullerton.edu)** (CWID: 886805050)
- **Luis Valle-Arellanes** (CWID: 889900429)

## Project Status

The project is actively maintained and follows best practices for Flask application development. Future enhancements may include:

- Advanced search functionality
- User profile management
- Rating analytics and statistics
- Enhanced admin dashboard

## Recording

[Recording of Completed App & Functionality](ttps://drive.google.com/file/d/1Szte0jPwRnGdVhyyQOagxNJYMM6n1f9u/view?usp=sharing)

---

## GitHub

[movie-rating-service](https://github.com/LemonmadeDesigns/movie-rating-service)
