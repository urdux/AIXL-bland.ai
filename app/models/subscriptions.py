from datetime import datetime
from app.database import db
from ..models.user import User  # Importing the User model

class Subscription(db.Model):
    __tablename__ = 'subscriptions'
    
    subscription_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    plan_name = db.Column(db.String(100), nullable=False)
    start_date = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    end_date = db.Column(db.Date, nullable=True)
    status = db.Column(db.String(50), nullable=False, default='active')

    user = db.relationship('User', back_populates='subscriptions')

    def __repr__(self):
        return f'<Subscription {self.plan_name} for User {self.user_id}>'


class Wallet(db.Model):
    __tablename__ = 'wallets'

    wallet_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    balance = db.Column(db.Numeric(10, 2), nullable=False, default=0.0)
    last_recharge = db.Column(db.DateTime, nullable=True)
    last_used = db.Column(db.DateTime, nullable=True)

    user = db.relationship('User', back_populates='wallet')

    def __repr__(self):
        return f'<Wallet Balance: {self.balance} for User {self.user_id}>'