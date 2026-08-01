#Instead of putting all endpoints inside main.py, every feature gets its own router.
# Each router will manage its own endpoints
# chat.py
# appointments.py
# customers.py
# health.py

from fastapi import APIRouter
from app.schemas.chat import ChatRequest, ChatResponse
from app.services.chat_service import ChatService
from app.schemas.booking import BookingRequest, BookingResponse
from app.services.booking_service import BookingService


router = APIRouter()

#User endpiint for chat with AI receptionist
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

# Appointment booking endpoint
@router.post("/booking",response_model=BookingResponse,tags=["Booking"])
def book_appointment(request:BookingRequest) -> dict:
    """
    Book an appointment.

    Args:
        request (BookingRequest): Appointment details.

    Returns:
        dict: Booking confirmation.
    """
    return BookingService.book_appointment(request)