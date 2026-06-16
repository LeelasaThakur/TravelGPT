import json
from app.llm.groq_client import groq_client
from app.llm.prompts import Prompts
from app.models import db, Conversation, Message
from app.services.booking_service import BookingService

class ChatService:
    @staticmethod
    def process_message(user_id: str, conversation_id: str, content: str) -> dict:
        """
        Main entry point for processing a user's chat message.
        """
        # 1. Fetch or create conversation
        conversation = Conversation.query.filter_by(id=conversation_id, user_id=user_id).first()
        if not conversation:
            conversation = Conversation(id=conversation_id, user_id=user_id)
            db.session.add(conversation)

        # 2. Save User Message
        user_msg = Message(conversation_id=conversation.id, role='user', content=content)
        db.session.add(user_msg)
        db.session.commit()

        # 3. Extract Intent using LLM
        intent_data = ChatService.extract_intent(content)
        intent = intent_data.get('intent', 'general_chat')
        details = intent_data.get('extracted_details', {})

        # 4. Handle based on intent
        response_data = {
            "intent": intent,
            "details": details,
            "reply": "",
            "requires_action": False,
            "options": []
        }

        if intent == "book_flight":
            reply, action, options = ChatService._handle_book_flight(details)
            response_data['reply'] = reply
            response_data['requires_action'] = action
            response_data['options'] = options
            
        elif intent == "book_hotel":
            reply, action, options = ChatService._handle_book_hotel(details)
            response_data['reply'] = reply
            response_data['requires_action'] = action
            response_data['options'] = options
            
        elif intent == "plan_itinerary":
            # For itinerary, we can just return a generated prompt
            dest = details.get('destination_city')
            if dest:
                reply = groq_client.generate_response([
                    {"role": "system", "content": Prompts.SYSTEM_ASSISTANT},
                    {"role": "user", "content": Prompts.itinerary_prompt(dest)}
                ])
                response_data['reply'] = reply
            else:
                response_data['reply'] = "Where would you like me to plan an itinerary for?"
                
        else:
            # General Chat fallback
            reply = groq_client.generate_response([
                {"role": "system", "content": Prompts.SYSTEM_ASSISTANT},
                {"role": "user", "content": content}
            ])
            response_data['reply'] = reply

        # 5. Save Assistant Message
        bot_msg = Message(conversation_id=conversation.id, role='assistant', content=response_data['reply'], metadata_json=response_data)
        db.session.add(bot_msg)
        db.session.commit()

        return response_data

    @staticmethod
    def extract_intent(content: str) -> dict:
        prompt = Prompts.extract_intent_prompt(content)
        response = groq_client.generate_response(
            messages=[{"role": "user", "content": prompt}],
            json_mode=True
        )
        try:
            return json.loads(response) if response else {}
        except json.JSONDecodeError:
            return {}

    @staticmethod
    def _handle_book_flight(details: dict):
        required = ['boarding_city', 'destination_city', 'travel_date', 'name', 'contact']
        missing = [req for req in required if not details.get(req)]
        
        if missing:
            return f"I can help you book a flight. Please provide the following missing details: {', '.join(missing)}.", False, []
            
        # All details present, search flights
        flights = BookingService.search_flights(
            details['boarding_city'], 
            details['destination_city'], 
            details['travel_date']
        )
        
        if not flights:
            return f"No flights found from {details['boarding_city']} to {details['destination_city']} on {details['travel_date']}.", False, []
            
        # We return the flights as options
        return "I found some flights. Please select one to book:", True, flights

    @staticmethod
    def _handle_book_hotel(details: dict):
        required = ['city_name', 'check_in_date', 'check_out_date', 'name', 'contact', 'adults']
        missing = [req for req in required if not details.get(req)]
        
        if missing:
            return f"I can help you book a hotel. Please provide the following missing details: {', '.join(missing)}.", False, []
            
        hotels = BookingService.search_hotels(
            details['city_name'], 
            details['check_in_date'], 
            details['check_out_date'],
            details.get('adults', 1)
        )
        
        if not hotels:
            return f"No hotels found in {details['city_name']} for those dates.", False, []
            
        return "I found these hotels. Please select one:", True, hotels
