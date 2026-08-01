#Instead of putting all endpoints inside main.py, every feature gets its own router.
# Each router will manage its own endpoints
# chat.py
# appointments.py
# customers.py
# health.py

from fastapi import APIRouter
from app.schemas.chat import ChatRequest, ChatResponse
from app.services.chat_service import ChatService

router = APIRouter()

@router.post("/chat",response_model=ChatResponse,tags=["Chat"])
def chat(request: ChatRequest) -> ChatResponse:
    """
    Handle incoming chat messages.

    Args:
        request (ChatRequest): User message.

    Returns:
        ChatResponse: Generated reply.
    """
    return ChatService.get_response(request.message)