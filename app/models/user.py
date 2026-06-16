from datetime import datetime
import uuid
from sqlalchemy.dialects.postgresql import UUID
from . import db

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    session_id = db.Column(db.String(255), unique=True, index=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_active = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    bookings = db.relationship('Booking', back_populates='user', cascade='all, delete-orphan')
    conversations = db.relationship('Conversation', back_populates='user', cascade='all, delete-orphan')
    preferences = db.relationship('UserPreference', uselist=False, back_populates='user', cascade='all, delete-orphan')

class UserPreference(db.Model):
    __tablename__ = 'user_preferences'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), unique=True, nullable=False)
    home_airport = db.Column(db.String(3))
    preferred_currency = db.Column(db.String(3), default='USD')
    dietary_requirements = db.Column(db.String(255))
    
    user = db.relationship('User', back_populates='preferences')

class ActivityLog(db.Model):
    __tablename__ = 'activity_logs'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=True) # Optional, can be unauthenticated
    action = db.Column(db.String(255), nullable=False)
    details = db.Column(db.JSON)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
