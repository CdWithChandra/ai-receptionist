from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas.booking import (
    AppointmentResponse,
    BookingRequest, 
    BookingResponse,
)
from app.schemas.chat import ChatRequest, ChatResponse
from app.services.booking_service import BookingService
from app.services.chat_service import ChatService

router = APIRouter()

# # User endpoint for chat with AI receptionist
@router.post(
    "/chat",
    response_model=ChatResponse,
    tags=["Chat"]
)

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
    tags=["Booking"]
)
def book_appointment(
    request: BookingRequest, 
    db: Session = Depends(get_db)

) -> BookingResponse:
    """
    Book an appointment.
    """
    return BookingService.book_appointment(request, db)

# Retrieve all appointments
@router.get(
    "/appointments",
    response_model=list[AppointmentResponse],
    tags=["Booking"],
)
def get_appointments(
    db: Session = Depends(get_db)
) -> list[AppointmentResponse]:
    """
    Retrieve all appointments.
    """
    return BookingService.get_appointments(db)
