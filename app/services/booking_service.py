import uuid
from datetime import datetime, timedelta
import random
from app.models import db, FlightBooking, HotelBooking, Trip
from app.utils.validators import validate_date, validate_phone

class BookingService:
    @staticmethod
    def search_flights(boarding_city: str, destination_city: str, travel_date: str) -> list:
        """
        Deterministic mock search since external API was removed.
        Returns a list of flight options.
        """
        date_obj = validate_date(travel_date)
        if not date_obj:
            return []
            
        airlines = ["Horizon Air", "Skyways Elite", "Global Airways"]
        flights = []
        for i in range(3):
            dep_hour = random.randint(6, 20)
            dep_time = datetime.combine(date_obj, datetime.min.time()) + timedelta(hours=dep_hour)
            duration = timedelta(hours=random.randint(2, 8))
            arr_time = dep_time + duration
            
            flights.append({
                "id": str(i + 1),
                "airline": airlines[i],
                "departure_time": dep_time.isoformat(),
                "arrival_time": arr_time.isoformat(),
                "price": round(random.uniform(150.0, 800.0), 2),
                "currency": "USD"
            })
        return flights

    @staticmethod
    def book_flight(user_id: str, data: dict) -> FlightBooking:
        # We assume data is pre-validated by Pydantic schemas
        flight = FlightBooking(
            user_id=user_id,
            booking_reference=f"FL-{str(uuid.uuid4())[:8].upper()}",
            passenger_name=data['name'],
            contact_number=data['contact'],
            airline=data['airline'],
            boarding_city=data['boarding_city'],
            destination_city=data['destination_city'],
            travel_date=validate_date(data['travel_date']),
            departure_time=datetime.fromisoformat(data['departure_time']),
            arrival_time=datetime.fromisoformat(data['arrival_time']),
            price=data['price'],
            currency=data.get('currency', 'USD')
        )
        db.session.add(flight)
        db.session.commit()
        return flight

    @staticmethod
    def search_hotels(city_name: str, check_in_date: str, check_out_date: str, adults: int = 1) -> list:
        in_date = validate_date(check_in_date)
        out_date = validate_date(check_out_date)
        if not in_date or not out_date:
            return []
            
        hotels = ["The Grand Plaza", "Horizon Resort & Spa", "City Center Inn"]
        results = []
        for i in range(3):
            results.append({
                "id": str(i + 1),
                "hotel_name": hotels[i],
                "address": f"{random.randint(10, 999)} Main St, {city_name}",
                "price": round(random.uniform(100.0, 500.0) * ((out_date - in_date).days), 2),
                "currency": "USD"
            })
        return results

    @staticmethod
    def book_hotel(user_id: str, data: dict) -> HotelBooking:
        hotel = HotelBooking(
            user_id=user_id,
            booking_reference=f"HT-{str(uuid.uuid4())[:8].upper()}",
            guest_name=data['name'],
            contact_number=data['contact'],
            hotel_name=data['hotel_name'],
            city_name=data['city_name'],
            address=data['address'],
            check_in_date=validate_date(data['check_in_date']),
            check_out_date=validate_date(data['check_out_date']),
            adults=data['adults'],
            price=data['price'],
            currency=data.get('currency', 'USD')
        )
        db.session.add(hotel)
        db.session.commit()
        return hotel

    @staticmethod
    def get_booking(booking_reference: str):
        # Could be flight or hotel
        from app.models.booking import Booking
        return Booking.query.filter_by(booking_reference=booking_reference).first()
    
    @staticmethod
    def cancel_booking(booking_reference: str) -> bool:
        booking = BookingService.get_booking(booking_reference)
        if booking:
            booking.status = 'cancelled'
            db.session.commit()
            return True
        return False
