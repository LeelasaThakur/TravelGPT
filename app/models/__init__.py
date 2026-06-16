from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .user import User, UserPreference, ActivityLog
from .booking import Trip, Booking, FlightBooking, HotelBooking
from .chat import Conversation, Message
