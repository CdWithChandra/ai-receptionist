#The service layer contains the application's business logic.
# book_appointment()
# cancel_appointment()
# reschedule_appointment()
from urllib import response 

from app.schemas.chat import ChatResponse

class ChatService:
    """
    Service class for handling chat-related operations.
    """
    @staticmethod
    def get_response(message:str) -> ChatResponse:
        """
        Generate a response for the user's message.
        """
        normalized_message = message.strip().lower()
        if not normalized_message:
            return ChatResponse(
                reply="Please enter a valid message."
            )
        intent=ChatService.detect_intent(normalized_message)
        return ChatService.build_response(intent)
    
    @staticmethod
    def get_response(message: str) -> ChatResponse:
        """
        Generate a reply based on the incoming message.

        Args:
            message (str): The incoming chat message.

        Returns:
            ChatResponse: The generated reply.
        """
        # Placeholder logic for generating a reply.
        # In a real implementation, this would involve calling an AI model or other logic.

        message = message.strip().lower()
        if not message:
            return ChatResponse(
                reply="Please provide a valid message."
                )
        if message in ["hi","hello","hey"]:
            return ChatResponse(
                reply="Hello! Welcome to AI Receptionist. How can I help you today?"
            )
        if "appointment" in message:
            return ChatResponse(
                reply="Sure! I'd be happy to help. What date would you like to book?"
            )
        if message in ["thanks", "thank you"]:
            return ChatResponse(
                reply="You're welcome! Let me know if there's anything else I can help with."
            )
        if message in ["bye","goodbye"]:
            return ChatResponse(
                reply="Goodbye! Have a wonderful day."
            )
        return ChatResponse(
             reply="I'm sorry, I didn't understand that. Could you please rephrase your request?"
             )
    
    @staticmethod
    def build_response(intent: str) -> ChatResponse:
        """
        Build a response based on the detected intent.

        Args:
            intent (str): The detected intent.

        Returns:
            ChatResponse: The generated response.
        """
        responses = {
            "greeting": "Hello! Welcome to AI Receptionist. How can I help you today?",
            "appointment": "Sure! I'd be happy to help. What date would you like to book?",
            "thanks": "You're welcome! Let me know if there's anything else I can help with.",
            "goodbye": "Goodbye! Have a wonderful day.",
            "unknown": "I'm sorry, I didn't understand that. Could you please rephrase your request?"
        }
        # Placeholder logic for building a response based on intent.
        # In a real implementation, this would involve more complex logic.
        return ChatResponse(
            reply=response[intent]
        )
