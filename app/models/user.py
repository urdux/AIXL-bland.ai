from datetime import datetime
from app.database import db

class User(db.Model):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(50), default='User')
    business_name = db.Column(db.String(255), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = db.Column(db.DateTime, nullable=True)
    is_active = db.Column(db.Boolean, default=True)

    permissions = db.relationship('UserPermission', back_populates='user')
    campaigns = db.relationship('Campaign', back_populates='creator')

    def __repr__(self):
        return f'<User {self.email}>'

    @property
    def active(self):
        return self.is_active

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.user_id)

class Permission(db.Model):
    __tablename__ = 'permissions'

    permission_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    role = db.Column(db.String(50), nullable=False)
    manage_sub_admins = db.Column(db.Boolean, default=False)
    manage_users = db.Column(db.Boolean, default=False)
    create_campaign = db.Column(db.Boolean, default=False)
    manage_calls = db.Column(db.Boolean, default=False)
    view_call_logs = db.Column(db.Boolean, default=False)
    manage_integrations = db.Column(db.Boolean, default=False)
    manage_subscriptions = db.Column(db.Boolean, default=False)
    manage_reports = db.Column(db.Boolean, default=False)

    user_permissions = db.relationship('UserPermission', back_populates='permission')

class UserPermission(db.Model):
    __tablename__ = 'user_permissions'

    user_permission_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    permission_id = db.Column(db.Integer, db.ForeignKey('permissions.permission_id'))

    user = db.relationship('User', back_populates='permissions')
    permission = db.relationship('Permission', back_populates='user_permissions')
