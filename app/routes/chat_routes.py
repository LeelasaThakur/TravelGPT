from flask import Blueprint, request, jsonify, session
from app.services.chat_service import ChatService
from app.schemas.requests import ChatMessageRequest
from app.schemas.responses import BaseAPIResponse, ChatResponse
from pydantic import ValidationError
import uuid
import logging

logger = logging.getLogger(__name__)
chat_bp = Blueprint('chat', __name__, url_prefix='/api/chat')

@chat_bp.route('/message', methods=['POST'])
def send_message():
    try:
        # Validate input
        data = request.get_json()
        validated_data = ChatMessageRequest(**data)
        
        # User session management
        if 'user_id' not in session:
            session['user_id'] = str(uuid.uuid4())
            
        user_id = session['user_id']
        conv_id = validated_data.conversation_id or str(uuid.uuid4())

        # Process message via Service
        result = ChatService.process_message(user_id, conv_id, validated_data.message)
        
        response_data = ChatResponse(
            reply=result['reply'],
            intent=result['intent'],
            requires_action=result['requires_action'],
            options=result['options']
        )
        
        return jsonify({
            "status": "success",
            "message": "Message processed",
            "data": response_data.model_dump(),
            "conversation_id": conv_id
        }), 200

    except ValidationError as e:
        logger.warning(f"Validation error: {e.errors()}")
        return jsonify({"status": "error", "message": "Invalid input format"}), 400
    except Exception as e:
        logger.exception("Error processing chat message")
        return jsonify({"status": "error", "message": "Internal server error"}), 500
