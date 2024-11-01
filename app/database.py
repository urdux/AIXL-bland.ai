from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError

db = SQLAlchemy()
bcrypt = Bcrypt()

def create_database():
    DATABASE_URL = 'mysql://root:root%401234@127.0.0.1:3306/'  # Root URL without database
    engine = create_engine(DATABASE_URL, echo=True)

    with engine.connect() as connection:
        connection.execute(text("CREATE DATABASE IF NOT EXISTS aixl;"))
        print("Database 'aixl' created or already exists.")

def init_app(app):
    db.init_app(app)
    with app.app_context():
        print("Attempting to create tables...")
        try:
            db.create_all()  # Create tables if they don't exist
            print("Database tables created successfully.")
        except OperationalError as e:
            print(f"Error creating tables: {e}")
