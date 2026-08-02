from app.ai.booking_agent import BookingAgent
from app.schemas.chat import ChatResponse

class ChatService:
    """
    Service class for handling chat-related operations.
    """
    def get_response(message: str) -> ChatResponse:
        """
        Generate a response for an incoming chat message.
        """
        reply = BookingAgent.process_message(message)
        return ChatResponse(reply=reply)
   