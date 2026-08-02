from app.ai.prompts import SYSTEM_PROMPT

class BookingAgent:
    """
    AI agent responsible for understanding
    user messages and generating responses.
    """

    @staticmethod
    def process_message(message: str) -> str:
        """
        Process an incoming user message.

        Args:
            message (str): User message.

        Returns:
            str: AI response.
        """
        message = message.strip().lower()

        if not message:
            return "Please enter a message."
        if any(word in message for word in ["hi", "hello", "hey"]):
            return (
               "Hello! Welcome to AI Receptionist. "
                "How can I help you today?"
            )
        if "book" in message:
            return (
                "Sure! I'd be happy to help you book an appointment."
            )
        if "appointment" in message and(
            "show" in message or "view" in message
        ):
            return (
                 "I can help you view your appointments."
            )
        if "update" in message:
            return (
                "I can help you update your appointment."
            )
        if "cancel" in message or "delete" in message:
            return (
                  "I can help you cancel your appointment."
            )
        return (
            "I'm sorry, I didn't understand your request."
        )