from flask import Blueprint, request, jsonify, session
from app.services.booking_service import BookingService
from app.schemas.requests import FlightBookingRequest, HotelBookingRequest
from pydantic import ValidationError
import logging
import uuid

logger = logging.getLogger(__name__)
booking_bp = Blueprint('booking', __name__, url_prefix='/api/booking')

@booking_bp.route('/flight', methods=['POST'])
def book_flight():
    try:
        data = request.get_json()
        validated_data = FlightBookingRequest(**data)
        
        if 'user_id' not in session:
            session['user_id'] = str(uuid.uuid4())
            
        booking = BookingService.book_flight(session['user_id'], validated_data.model_dump())
        
        return jsonify({
            "status": "success",
            "message": "Flight booked successfully",
            "data": {
                "booking_reference": booking.booking_reference,
                "airline": booking.airline,
                "price": booking.price
            }
        }), 201
        
    except ValidationError as e:
        logger.warning(f"Validation error: {e.errors()}")
        return jsonify({"status": "error", "message": "Invalid input format"}), 400
    except Exception as e:
        logger.exception("Error booking flight")
        return jsonify({"status": "error", "message": "Internal server error"}), 500

@booking_bp.route('/hotel', methods=['POST'])
def book_hotel():
    try:
        data = request.get_json()
        validated_data = HotelBookingRequest(**data)
        
        if 'user_id' not in session:
            session['user_id'] = str(uuid.uuid4())
            
        booking = BookingService.book_hotel(session['user_id'], validated_data.model_dump())
        
        return jsonify({
            "status": "success",
            "message": "Hotel booked successfully",
            "data": {
                "booking_reference": booking.booking_reference,
                "hotel_name": booking.hotel_name,
                "price": booking.price
            }
        }), 201
        
    except ValidationError as e:
        logger.warning(f"Validation error: {e.errors()}")
        return jsonify({"status": "error", "message": "Invalid input format"}), 400
    except Exception as e:
        logger.exception("Error booking hotel")
        return jsonify({"status": "error", "message": "Internal server error"}), 500

@booking_bp.route('/<reference>', methods=['GET'])
def get_booking(reference):
    try:
        booking = BookingService.get_booking(reference)
        if not booking:
            return jsonify({"status": "error", "message": "Booking not found"}), 404
            
        return jsonify({
            "status": "success",
            "data": {
                "booking_reference": booking.booking_reference,
                "type": booking.booking_type,
                "status": booking.status,
                "price": booking.price
            }
        }), 200
    except Exception as e:
        logger.exception("Error fetching booking")
        return jsonify({"status": "error", "message": "Internal server error"}), 500
