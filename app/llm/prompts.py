import json

class Prompts:
    SYSTEM_ASSISTANT = """
    You are Horizon, an elite, highly intelligent, and luxurious AI travel concierge.
    You assist users in planning trips, providing itineraries, booking flights, and booking hotels.
    Your tone should be professional, welcoming, precise, and slightly sophisticated.
    
    When discussing travel options, present them clearly, often using markdown lists or bolding key terms.
    If a user wants to book a flight or hotel, guide them step-by-step through gathering the required details if any are missing.
    Always be polite and extremely helpful.
    """

    @staticmethod
    def extract_intent_prompt(user_message: str) -> str:
        return f"""
        Analyze the user's input and extract the intent and any travel details.
        
        Possible Intents:
        - "book_flight": User wants to book a flight.
        - "book_hotel": User wants to book a hotel.
        - "update_flight": User wants to modify an existing flight.
        - "update_hotel": User wants to modify an existing hotel booking.
        - "fetch_flight": User wants to see flight booking details.
        - "fetch_hotel": User wants to see hotel booking details.
        - "cancel_flight": User wants to cancel a flight.
        - "cancel_hotel": User wants to cancel a hotel.
        - "plan_itinerary": User wants a travel itinerary or suggestions.
        - "general_chat": Any other conversational input.

        Extract details if present (leave null if not found):
        - boarding_city
        - destination_city
        - travel_date (YYYY-MM-DD)
        - name
        - contact
        - check_in_date
        - check_out_date
        - adults (integer)
        - booking_id (or flight_id)

        Output ONLY valid JSON matching this schema:
        {{
            "intent": "string",
            "extracted_details": {{
                "boarding_city": "string | null",
                "destination_city": "string | null",
                "travel_date": "string | null",
                "name": "string | null",
                "contact": "string | null",
                "check_in_date": "string | null",
                "check_out_date": "string | null",
                "adults": "integer | null",
                "booking_id": "string | null"
            }}
        }}

        User Input: "{user_message}"
        """

    @staticmethod
    def itinerary_prompt(destination: str, days: int = 3) -> str:
        return f"""
        Create a luxurious, well-paced travel itinerary for {destination} for {days} days.
        Format your response beautifully using Markdown.
        For each day, provide a Morning, Afternoon, and Evening section.
        Include specific recommendations for attractions and dining.
        Do not make the schedule overly exhausting. Add travel tips at the end.
        """
