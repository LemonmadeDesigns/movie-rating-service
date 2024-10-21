# config.py
import os
import urllib.parse

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'your_secret_key')
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres'+ '@localhost/movie_rating_service'
    SQLALCHEMY_TRACK_MODIFICATIONS = False