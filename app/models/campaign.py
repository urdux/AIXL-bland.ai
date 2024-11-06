# models/campaign.py
from datetime import datetime
from app.database import db
from .user import User  # Import User model for ForeignKey relationships

class Campaign(db.Model):
    __tablename__ = 'campaigns'

    campaign_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    campaign_name = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    greeting = db.Column(db.Text)
    prompt = db.Column(db.Text)
    call_numbers = db.Column(db.Text)
    routing_group = db.Column(db.String(100))
    campaign_type = db.Column(db.String(10), nullable=False)  # 'inbound' or 'outbound'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = db.relationship('User', back_populates='campaigns')
    knowledge_base = db.relationship('KnowledgeBase', back_populates='campaign', cascade='all, delete-orphan')  # Set cascade for knowledge bases
    scheduled_calls = db.relationship('ScheduledCall', back_populates='campaign', cascade='all, delete-orphan')  # Set cascade for scheduled calls
    agents = db.relationship('Agent', back_populates='campaign', cascade='all, delete-orphan')  # Set cascade for agents
    campaign_agents = db.relationship('CampaignAgent', back_populates='campaign', cascade='all, delete-orphan')  # Set cascade for campaign agents


class KnowledgeBase(db.Model):
    __tablename__ = 'knowledge_base'

    kb_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    campaign_id = db.Column(db.Integer, db.ForeignKey('campaigns.campaign_id', ondelete='CASCADE'))  # Add ondelete='CASCADE'
    faq_entries = db.Column(db.JSON)  # JSON format for multiple FAQ entries
    data_source = db.Column(db.Text)
    knowledge_base = db.Column(db.Text)
    pinecone_index = db.Column(db.String(255))
    pinecone_api = db.Column(db.String(255))
    last_updated = db.Column(db.DateTime, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    campaign = db.relationship('Campaign', back_populates='knowledge_base')


class Agent(db.Model):
    __tablename__ = 'agents'

    agent_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    agent_name = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(50))
    campaign_id = db.Column(db.Integer, db.ForeignKey('campaigns.campaign_id', ondelete='CASCADE'))  # Foreign key with cascade delete

    campaign = db.relationship('Campaign', back_populates='agents')


class CampaignAgent(db.Model):
    __tablename__ = 'campaign_agents'

    campaign_agent_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    campaign_id = db.Column(db.Integer, db.ForeignKey('campaigns.campaign_id', ondelete='CASCADE'), nullable=False)  # Add ondelete='CASCADE'
    agent_id = db.Column(db.Integer, db.ForeignKey('agents.agent_id'), nullable=False)
    phone_number = db.Column(db.String(15), nullable=False)

    campaign = db.relationship('Campaign', back_populates='campaign_agents')


class ScheduledCall(db.Model):
    __tablename__ = 'scheduled_calls'

    scheduled_call_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    campaign_id = db.Column(db.Integer, db.ForeignKey('campaigns.campaign_id', ondelete='CASCADE'), nullable=False)  # Add ondelete='CASCADE'
    date_from = db.Column(db.Date, nullable=False)
    time_from = db.Column(db.Time, nullable=False)
    date_to = db.Column(db.Date, nullable=False)
    time_to = db.Column(db.Time, nullable=False)
    status = db.Column(db.String(50), nullable=False)  # 'scheduled', 'completed', 'cancelled'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    campaign = db.relationship('Campaign', back_populates='scheduled_calls')
