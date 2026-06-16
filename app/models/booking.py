from datetime import datetime
import uuid
from . import db

class Trip(db.Model):
    __tablename__ = 'trips'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    destination = db.Column(db.String(255), nullable=False)
    start_date = db.Column(db.Date, nullable=True)
    end_date = db.Column(db.Date, nullable=True)
    status = db.Column(db.String(50), default='planning') # planning, booked, completed, cancelled
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    bookings = db.relationship('Booking', back_populates='trip', cascade='all, delete-orphan')

class Booking(db.Model):
    __tablename__ = 'bookings'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    trip_id = db.Column(db.String(36), db.ForeignKey('trips.id'), nullable=True)
    booking_type = db.Column(db.String(50), nullable=False) # flight, hotel
    status = db.Column(db.String(50), default='confirmed') # confirmed, cancelled
    booking_reference = db.Column(db.String(50), unique=True, nullable=False)
    price = db.Column(db.Float)
    currency = db.Column(db.String(3), default='USD')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    user = db.relationship('User', back_populates='bookings')
    trip = db.relationship('Trip', back_populates='bookings')
    
    __mapper_args__ = {
        'polymorphic_on': booking_type,
        'polymorphic_identity': 'booking'
    }

class FlightBooking(Booking):
    __tablename__ = 'flight_bookings'
    
    id = db.Column(db.String(36), db.ForeignKey('bookings.id'), primary_key=True)
    passenger_name = db.Column(db.String(255), nullable=False)
    contact_number = db.Column(db.String(50), nullable=False)
    airline = db.Column(db.String(255), nullable=False)
    boarding_city = db.Column(db.String(100), nullable=False)
    destination_city = db.Column(db.String(100), nullable=False)
    travel_date = db.Column(db.Date, nullable=False)
    departure_time = db.Column(db.DateTime, nullable=False)
    arrival_time = db.Column(db.DateTime, nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': 'flight',
    }

class HotelBooking(Booking):
    __tablename__ = 'hotel_bookings'
    
    id = db.Column(db.String(36), db.ForeignKey('bookings.id'), primary_key=True)
    guest_name = db.Column(db.String(255), nullable=False)
    contact_number = db.Column(db.String(50), nullable=False)
    hotel_name = db.Column(db.String(255), nullable=False)
    city_name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.Text)
    check_in_date = db.Column(db.Date, nullable=False)
    check_out_date = db.Column(db.Date, nullable=False)
    adults = db.Column(db.Integer, default=1)

    __mapper_args__ = {
        'polymorphic_identity': 'hotel',
    }
