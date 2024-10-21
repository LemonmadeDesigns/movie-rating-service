# Movie Rating Service

This project is a **Movie Rating Service** built with Flask. It allows users to register, authenticate, add movies, submit ratings, and view movie details. The service also supports file uploads with restricted file extensions.

## Project Features

### 1. User Authentication

- **User Registration**: Users (admin and regular) can sign up via a registration endpoint.
- **User Login**: JWT-based authentication for login and token generation.

### 2. Movie Management (Admin Only)

- **Add Movie**: Admins can add a new movie to the database.
- **Delete Movie Ratings**: Admins can delete any user's rating for a movie.

### 3. User Ratings

- **Submit Rating**: Users can rate a movie that exists in the database.
- **Update Rating**: Users can update their own ratings.
- **Delete Rating**: Users can delete their own ratings.
- **Retrieve Ratings**: Retrieve all user ratings for all movies.
- **Fetch Movie Details**: Retrieve details for a specific movie, including user ratings.

### 4. File Upload

- A separate API supports file uploads and restricts the allowed file extensions. Supported extensions include `.jpg`, `.png`, and `.pdf`.

## Technology Stack

- **Backend**: Flask (Python)
- **Frontend**: HTML
- **Authentication**: JWT (JSON Web Token)
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy
- **Environment**: Virtualenv for dependency management

## Installation Guide

1. Clone the repository:

   ```bash
   git clone https://github.com/LemonmadeDesigns/movie-rating-service.git
   cd movie-rating-service
   ```

2. Create a virtual environment and activate it:

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # For Linux/Mac
   venv\Scripts\activate  # For Windows
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables (e.g., for JWT secret key):

   ```bash
   export FLASK_APP=app.py
   export JWT_SECRET_KEY='your_jwt_secret_key'
   ```

5. Run the Flask application:

   ```bash
   flask run
   ```

6. Use Postman or cURL to interact with the API.

## API Endpoints

### **User Authentication**

- `POST /register`: Register a new user (admin or regular user).
- `POST /login`: Login and receive a JWT token.

### **Movie Management (Admin)**

- `POST /movies`: Add a new movie (admin-only).
- `DELETE /ratings/{movie_id}/{user_id}`: Admin can delete any user’s rating.

### **User Ratings**

- `POST /movies/{movie_id}/rate`: Rate a movie.
- `PUT /movies/{movie_id}/rate`: Update user rating.
- `DELETE /movies/{movie_id}/rate`: Delete user rating.
- `GET /ratings`: Get all user ratings.
- `GET /movies/{movie_id}`: Get details of a specific movie, including its ratings.

### **File Upload**

- `POST /upload`: Upload a file (allowed extensions: `.jpg`, `.png`, `.pdf`).

## Testing

- Use **Postman** to test the API endpoints.
- Run the following command to execute the unit tests (if implemented):

  ```bash
  python -m unittest discover
  ```

## Recording and Submission

- [] Record your screen using a screen recorder (OBS Studio or any other tool) to showcase the code and Postman requests.
- [x] Upload the recording as part of the submission.
- [x] Provide the GitHub repository link.

## Contributors

This project was developed collaboratively by the following team members:

- **Terrell D Lemons** (CWID: 886659440)
- **Kyle Williams** (CWID: 886805050)
- **Luis Valle-Arellanes** (CWID: 889900429)

## Contribution

Feel free to fork this repository and submit pull requests. Any improvements or suggestions are welcome!

## License

This project is licensed under the MIT License. See the LICENSE file for details.

---

[movie-rating-service](https://github.com/LemonmadeDesigns/movie-rating-service)
