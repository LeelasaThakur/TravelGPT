from datetime import datetime
import phonenumbers
from typing import Optional

def validate_date(date_str: str) -> Optional[datetime.date]:
    """
    Parses and validates a date string.
    Returns datetime.date object or None if invalid.
    """
    if not date_str:
        return None
    
    formats = ["%Y-%m-%d", "%d-%m-%Y", "%m/%d/%Y"]
    for fmt in formats:
        try:
            return datetime.strptime(date_str.strip(), fmt).date()
        except ValueError:
            continue
    return None

def validate_phone(contact: str) -> Optional[str]:
    """
    Validates and formats a phone number.
    Returns E164 format or None if invalid.
    """
    if not contact:
        return None
    try:
        parsed_number = phonenumbers.parse(contact, "IN") # Defaulting to IN as original
        if phonenumbers.is_valid_number(parsed_number):
            return phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.E164)
    except phonenumbers.phonenumberutil.NumberParseException:
        pass
    return None
