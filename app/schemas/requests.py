from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime

class ChatMessageRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=2000)
    conversation_id: Optional[str] = None

class FlightBookingRequest(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    contact: str = Field(..., min_length=10, max_length=20)
    boarding_city: str = Field(..., min_length=2, max_length=50)
    destination_city: str = Field(..., min_length=2, max_length=50)
    travel_date: str
    airline: str
    departure_time: str
    arrival_time: str
    price: float
    currency: str = "USD"

class HotelBookingRequest(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    contact: str = Field(..., min_length=10, max_length=20)
    city_name: str = Field(..., min_length=2, max_length=50)
    hotel_name: str
    address: str
    check_in_date: str
    check_out_date: str
    adults: int = Field(ge=1, le=10)
    price: float
    currency: str = "USD"
