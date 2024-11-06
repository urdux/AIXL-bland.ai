from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from datetime import datetime

# Setup Flask app and database
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root%401234@127.0.0.1:3306/aixl'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

# Define User model
class User(db.Model):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(50), default='User')
    business_name = db.Column(db.String(255), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# Create the super admin user
def create_super_admin():
    # Hash the password
    hashed_password = bcrypt.generate_password_hash('shahbaz@1234').decode('utf-8')
    
    # Create a new super admin user
    super_admin = User(
        email='shabaz12@gmail.com',
        password=hashed_password,
        role='Super Admin',  # Set role to Super Admin
        business_name='SuperAdmin Business',
        address='123 Admin St',
        city='Admin City',
        phone_number='1234567890'
    )
    
    # Add and commit to the database
    db.create_all()  # Ensure all tables are created
    db.session.add(super_admin)
    db.session.commit()
    print("Super admin created successfully!")

# Run the function to create the super admin
with app.app_context():
    create_super_admin()
