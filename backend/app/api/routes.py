#Instead of putting all endpoints inside main.py, every feature gets its own router.
# Each router will manage its own endpoints
# chat.py
# appointments.py
# customers.py
# health.py

from fastapi import APIRouter, Depends
from httpx import request
from app.schemas.chat import ChatRequest, ChatResponse
from app.services.chat_service import ChatService
from app.schemas.booking import BookingRequest, BookingResponse
from app.services.booking_service import BookingService
from sqlalchemy.orm import Session
from app.database.session import get_db


router = APIRouter()

#User endpiint for chat with AI receptionist
@router.post(
        "/chat",
        response_model=ChatResponse,
        tags=["Chat"])

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
@router.post(
        "/booking",
        response_model=BookingResponse,
        tags=["Booking"])
def book_appointment(
    request: BookingRequest, 
    db: Session = Depends(get_db)

) -> BookingResponse:
    """
    Book an appointment.
    """
    return BookingService.book_appointment(request, db)