from app.ai.prompts import SYSTEM_PROMPT
from app.schemas.chat import ChatIntent

class BookingAgent:
    """
    AI agent responsible for understanding
    user messages and detecting user intent.
    """

    @staticmethod
    def process_message(message: str) -> str:
        """
        Detect the user's intent.

        Args:
           message (str): User message.

        Returns:
           ChatIntent: Detected intent.
        """
        message = message.strip().lower()

        if not message:
            return ChatIntent(intent="empty")

        if any(word in message for word in ["hi", "hello", "hey"]):
            return ChatIntent(intent="greeting")

        if "book" in message:
            return ChatIntent(intent="book_appointment")

        if "appointment" in message and (
            "show" in message or "view" in message
        ):
            return ChatIntent(intent="show_appointments")

        if "update" in message:
            return ChatIntent(intent="update_appointment")

        if "cancel" in message or "delete" in message:
            return ChatIntent(intent="cancel_appointment")

        return ChatIntent(intent="unknown")
