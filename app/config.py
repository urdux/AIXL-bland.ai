import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'you-will-never-guess')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'mysql://root:root%401234@127.0.0.1:3306/aixl')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
