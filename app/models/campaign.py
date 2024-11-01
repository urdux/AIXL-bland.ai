from datetime import datetime
from app.database import db

class Campaign(db.Model):
    __tablename__ = 'campaigns'

    campaign_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    assigned_phone_numbers = db.Column(db.JSON, nullable=True)
    custom_faq = db.Column(db.Boolean, default=False)
    knowledge_base = db.Column(db.Text, nullable=True)
    data_source_type = db.Column(db.Enum('API', 'flat_file', 'database'), nullable=False)
    data_source_details = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    creator = db.relationship('User', back_populates='campaigns')

    def __repr__(self):
        return f'<Campaign {self.name}>'
