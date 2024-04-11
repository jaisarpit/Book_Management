from datetime import timedelta
import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')  # Replace with your DB credentials
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get('SECRET_KEY')  # Replace with your secret key
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=1)
