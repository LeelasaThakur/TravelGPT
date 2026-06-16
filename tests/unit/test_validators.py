from app.utils.validators import validate_date, validate_phone
import datetime

def test_validate_date_valid():
    assert validate_date("2024-05-15") == datetime.date(2024, 5, 15)
    assert validate_date("15-05-2024") == datetime.date(2024, 5, 15)
    assert validate_date("05/15/2024") == datetime.date(2024, 5, 15)

def test_validate_date_invalid():
    assert validate_date("invalid_date") is None
    assert validate_date("2024-15-05") is None

def test_validate_phone_valid():
    # Example valid Indian number format 
    assert validate_phone("+919876543210") == "+919876543210"

def test_validate_phone_invalid():
    assert validate_phone("123") is None
    assert validate_phone("invalid_phone") is None
