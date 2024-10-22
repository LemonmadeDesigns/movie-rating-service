# config.py
import os
import urllib.parse

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'your_secret_key')
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:postgres@localhost/movie_rating_service'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
